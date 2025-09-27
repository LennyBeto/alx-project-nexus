// src/hooks/useComments.js
import { useState, useCallback } from 'react';
import { useQuery, useMutation, useApolloClient } from '@apollo/client';
import { 
  GET_POST_DETAILS, 
  CREATE_COMMENT, 
  LIKE_COMMENT,
  GET_POSTS,
  GET_FEED
} from '../graphql/queries';

/**
 * Custom hook for managing comments on a specific post
 * @param {number} postId - The ID of the post to manage comments for
 */
export const useComments = (postId) => {
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const limit = 20;
  const client = useApolloClient();

  // Query for post details and comments
  const { 
    data, 
    loading, 
    error, 
    refetch, 
    fetchMore 
  } = useQuery(GET_POST_DETAILS, {
    variables: { postId: parseInt(postId) },
    skip: !postId,
    errorPolicy: 'all',
    notifyOnNetworkStatusChange: true,
    onCompleted: (data) => {
      if (data?.comments && data.comments.length < limit) {
        setHasMore(false);
      }
    }
  });

  // Mutation for creating comments
  const [createCommentMutation] = useMutation(CREATE_COMMENT, {
    onError: (error) => {
      console.error('Create comment error:', error);
    },
    update: (cache, { data: { createComment } }) => {
      if (createComment.success && createComment.comment) {
        // Update the post details cache
        try {
          const existingData = cache.readQuery({
            query: GET_POST_DETAILS,
            variables: { postId: parseInt(postId) }
          });

          if (existingData) {
            cache.writeQuery({
              query: GET_POST_DETAILS,
              variables: { postId: parseInt(postId) },
              data: {
                ...existingData,
                comments: [createComment.comment, ...existingData.comments],
                post: {
                  ...existingData.post,
                  commentsCount: existingData.post.commentsCount + 1
                }
              }
            });
          }
        } catch (error) {
          console.log('Cache update error (non-critical):', error);
        }

        // Update posts/feed cache to reflect new comment count
        updatePostsCache(postId, 'increment');
      }
    }
  });

  // Mutation for liking comments
  const [likeCommentMutation] = useMutation(LIKE_COMMENT, {
    onError: (error) => {
      console.error('Like comment error:', error);
    },
    optimisticResponse: ({ commentId }) => ({
      likeComment: {
        success: true,
        message: 'Comment liked',
        __typename: 'LikeComment'
      }
    })
  });

  /**
   * Update posts cache with new comment count
   * @param {number} postId - Post ID to update
   * @param {string} action - 'increment' or 'decrement'
   */
  const updatePostsCache = useCallback((postId, action) => {
    const queries = [
      { query: GET_POSTS, variables: { limit: 20, offset: 0 } },
      { query: GET_FEED, variables: { limit: 20, offset: 0 } }
    ];

    queries.forEach(({ query, variables }) => {
      try {
        const existingData = client.readQuery({ query, variables });
        if (existingData) {
          const field = query === GET_FEED ? 'feed' : 'posts';
          const updatedPosts = existingData[field].map(post => {
            if (post.id === postId.toString()) {
              return {
                ...post,
                commentsCount: action === 'increment' 
                  ? post.commentsCount + 1 
                  : Math.max(0, post.commentsCount - 1)
              };
            }
            return post;
          });

          client.writeQuery({
            query,
            variables,
            data: { [field]: updatedPosts }
          });
        }
      } catch (error) {
        // Cache update is non-critical
        console.log('Cache update error (non-critical):', error);
      }
    });
  }, [client]);

  /**
   * Create a new comment on the post
   * @param {string} content - Comment content
   * @param {number} parentId - Parent comment ID for replies (optional)
   * @returns {Object} Result object with success status
   */
  const createComment = async (content, parentId = null) => {
    try {
      if (!content.trim()) {
        throw new Error('Comment content cannot be empty');
      }

      const result = await createCommentMutation({
        variables: {
          postId: parseInt(postId),
          content: content.trim(),
          parentId: parentId ? parseInt(parentId) : null,
        },
      });

      if (result.data.createComment.success) {
        return {
          success: true,
          comment: result.data.createComment.comment,
          message: result.data.createComment.message
        };
      } else {
        throw new Error(result.data.createComment.message || 'Failed to create comment');
      }
    } catch (error) {
      console.error('Error creating comment:', error);
      return {
        success: false,
        error: error.graphQLErrors?.[0]?.message || error.message || 'Failed to create comment'
      };
    }
  };

  /**
   * Like or unlike a comment
   * @param {number} commentId - Comment ID to like
   * @returns {Object} Result object with success status
   */
  const likeComment = async (commentId) => {
    try {
      const result = await likeCommentMutation({
        variables: { commentId: parseInt(commentId) },
      });

      return {
        success: result.data.likeComment.success,
        message: result.data.likeComment.message
      };
    } catch (error) {
      console.error('Error liking comment:', error);
      return {
        success: false,
        error: error.graphQLErrors?.[0]?.message || error.message || 'Failed to like comment'
      };
    }
  };

  /**
   * Load more comments (pagination)
   */
  const loadMoreComments = useCallback(async () => {
    if (!hasMore || loading) return;

    try {
      const result = await fetchMore({
        variables: {
          postId: parseInt(postId),
          offset: data?.comments?.length || 0,
          limit,
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          if (!fetchMoreResult || !fetchMoreResult.comments) {
            return previousResult;
          }

          const newComments = fetchMoreResult.comments;
          
          if (newComments.length < limit) {
            setHasMore(false);
          }

          return {
            ...previousResult,
            comments: [...previousResult.comments, ...newComments],
          };
        },
      });
    } catch (error) {
      console.error('Error loading more comments:', error);
    }
  }, [data?.comments?.length, fetchMore, hasMore, loading, limit, postId]);

  /**
   * Refresh comments data
   */
  const refreshComments = useCallback(async () => {
    setOffset(0);
    setHasMore(true);
    
    try {
      await refetch();
    } catch (error) {
      console.error('Error refreshing comments:', error);
    }
  }, [refetch]);

  /**
   * Get comment by ID
   * @param {number} commentId - Comment ID to find
   * @returns {Object|null} Comment object or null if not found
   */
  const getCommentById = useCallback((commentId) => {
    if (!data?.comments) return null;
    
    return data.comments.find(comment => 
      comment.id === commentId.toString() || comment.id === commentId
    );
  }, [data?.comments]);

  /**
   * Get replies for a specific comment
   * @param {number} parentId - Parent comment ID
   * @returns {Array} Array of reply comments
   */
  const getReplies = useCallback((parentId) => {
    if (!data?.comments) return [];
    
    return data.comments.filter(comment => 
      comment.parent && (comment.parent.id === parentId.toString() || comment.parent.id === parentId)
    );
  }, [data?.comments]);

  /**
   * Get top-level comments (not replies)
   * @returns {Array} Array of top-level comments
   */
  const getTopLevelComments = useCallback(() => {
    if (!data?.comments) return [];
    
    return data.comments.filter(comment => !comment.parent);
  }, [data?.comments]);

  return {
    // Data
    post: data?.post,
    comments: data?.comments || [],
    topLevelComments: getTopLevelComments(),
    
    // State
    loading,
    error,
    hasMore,
    
    // Operations
    createComment,
    likeComment,
    loadMoreComments,
    refreshComments,
    refetch,
    
    // Utility functions
    getCommentById,
    getReplies,
    getTopLevelComments,
  };
};

/**
 * Hook for managing comment form state
 */
export const useCommentForm = () => {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [replyingTo, setReplyingTo] = useState(null);

  /**
   * Submit comment
   * @param {Function} submitFunction - Function to submit the comment
   * @returns {Object} Result of submission
   */
  const submitComment = async (submitFunction) => {
    if (!content.trim()) {
      return { success: false, error: 'Comment cannot be empty' };
    }

    setIsSubmitting(true);
    
    try {
      const result = await submitFunction(content, replyingTo?.id);
      
      if (result.success) {
        setContent('');
        setReplyingTo(null);
      }
      
      return result;
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Start replying to a comment
   * @param {Object} comment - Comment object to reply to
   */
  const startReply = (comment) => {
    setReplyingTo(comment);
  };

  /**
   * Cancel reply
   */
  const cancelReply = () => {
    setReplyingTo(null);
  };

  /**
   * Clear form
   */
  const clearForm = () => {
    setContent('');
    setReplyingTo(null);
  };

  return {
    content,
    setContent,
    isSubmitting,
    replyingTo,
    startReply,
    cancelReply,
    clearForm,
    submitComment,
  };
};

/**
 * Hook for comment interactions (like, reply counts)
 */
export const useCommentInteractions = (commentId) => {
  const [optimisticLike, setOptimisticLike] = useState(null);

  /**
   * Handle optimistic like update
   * @param {boolean} isLiked - Current like state
   */
  const handleOptimisticLike = (isLiked) => {
    setOptimisticLike(!isLiked);
    
    // Reset optimistic state after a delay
    setTimeout(() => {
      setOptimisticLike(null);
    }, 2000);
  };

  return {
    optimisticLike,
    handleOptimisticLike,
  };
};
