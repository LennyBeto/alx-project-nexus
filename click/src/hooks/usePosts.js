// src/hooks/usePosts.js
import { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import {
  GET_POSTS,
  GET_FEED,
  CREATE_POST,
  LIKE_POST,
  SHARE_POST,
} from "../graphql/queries";

export const usePosts = (useFeed = false) => {
  const [offset, setOffset] = useState(0);
  const limit = 20;

  const { data, loading, error, refetch, fetchMore } = useQuery(
    useFeed ? GET_FEED : GET_POSTS,
    {
      variables: { limit, offset: 0 },
      errorPolicy: "all",
      notifyOnNetworkStatusChange: true,
    }
  );

  const [createPost] = useMutation(CREATE_POST, {
    refetchQueries: [
      {
        query: useFeed ? GET_FEED : GET_POSTS,
        variables: { limit, offset: 0 },
      },
    ],
    onError: (error) => {
      console.error("Create post error:", error);
    },
  });

  const [likePost] = useMutation(LIKE_POST, {
    optimisticResponse: ({ postId }) => ({
      likePost: {
        success: true,
        message: "Post liked",
        __typename: "LikePost",
      },
    }),
    onError: (error) => {
      console.error("Like post error:", error);
    },
  });

  const [sharePost] = useMutation(SHARE_POST, {
    onError: (error) => {
      console.error("Share post error:", error);
    },
  });

  const posts = data ? (useFeed ? data.feed : data.posts) : [];

  const loadMore = () => {
    if (!loading) {
      fetchMore({
        variables: {
          offset: posts.length,
          limit,
        },
      });
    }
  };

  const handleCreatePost = async (content, imageUrl = null) => {
    try {
      const result = await createPost({
        variables: { content, imageUrl },
      });
      return result.data.createPost;
    } catch (error) {
      console.error("Error creating post:", error);
      throw error;
    }
  };

  const handleLikePost = async (postId) => {
    try {
      await likePost({
        variables: { postId: parseInt(postId) },
      });
    } catch (error) {
      console.error("Error liking post:", error);
      throw error;
    }
  };

  const handleSharePost = async (postId, message = null) => {
    try {
      const result = await sharePost({
        variables: { postId: parseInt(postId), message },
      });
      return result.data.sharePost;
    } catch (error) {
      console.error("Error sharing post:", error);
      throw error;
    }
  };

  return {
    posts,
    loading,
    error,
    refetch,
    loadMore,
    createPost: handleCreatePost,
    likePost: handleLikePost,
    sharePost: handleSharePost,
  };
};

// src/hooks/useAuth.js
import { useState } from "react";
import { useMutation } from "@apollo/client";
import { LOGIN_USER, REGISTER_USER } from "../graphql/queries";
import { useAuth as useAuthContext } from "../context/AuthContext";

export const useAuthMutations = () => {
  const [loading, setLoading] = useState(false);
  const { login: contextLogin } = useAuthContext();

  const [loginMutation] = useMutation(LOGIN_USER, {
    onError: (error) => {
      console.error("Login error:", error);
    },
  });

  const [registerMutation] = useMutation(REGISTER_USER, {
    onError: (error) => {
      console.error("Register error:", error);
    },
  });

  const login = async (username, password) => {
    setLoading(true);
    try {
      const result = await loginMutation({
        variables: { username, password },
      });

      if (result.data.loginUser.success) {
        await contextLogin(
          result.data.loginUser.token,
          result.data.loginUser.user
        );
        return { success: true, user: result.data.loginUser.user };
      } else {
        throw new Error(result.data.loginUser.message);
      }
    } catch (error) {
      console.error("Login failed:", error);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    setLoading(true);
    try {
      const result = await registerMutation({
        variables: userData,
      });

      if (result.data.registerUser.success) {
        await contextLogin(
          result.data.registerUser.token,
          result.data.registerUser.user
        );
        return { success: true, user: result.data.registerUser.user };
      } else {
        throw new Error(result.data.registerUser.message);
      }
    } catch (error) {
      console.error("Registration failed:", error);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  return {
    login,
    register,
    loading,
  };
};

// src/hooks/useComments.js
import { useQuery, useMutation } from "@apollo/client";
import { GET_POST_DETAILS, CREATE_COMMENT } from "../graphql/queries";

export const useComments = (postId) => {
  const { data, loading, error, refetch } = useQuery(GET_POST_DETAILS, {
    variables: { postId: parseInt(postId) },
    skip: !postId,
  });

  const [createComment] = useMutation(CREATE_COMMENT, {
    refetchQueries: [
      { query: GET_POST_DETAILS, variables: { postId: parseInt(postId) } },
    ],
  });

  const handleCreateComment = async (content, parentId = null) => {
    try {
      const result = await createComment({
        variables: {
          postId: parseInt(postId),
          content,
          parentId: parentId ? parseInt(parentId) : null,
        },
      });
      return result.data.createComment;
    } catch (error) {
      console.error("Error creating comment:", error);
      throw error;
    }
  };

  return {
    post: data?.post,
    comments: data?.comments || [],
    loading,
    error,
    refetch,
    createComment: handleCreateComment,
  };
};
