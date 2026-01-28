// hooks/usePostInteraction.ts

import { useState, useCallback } from "react";
import { useMutation } from "@apollo/client";
import {
  LIKE_POST,
  UNLIKE_POST,
  ADD_COMMENT,
  SHARE_POST,
  BOOKMARK_POST,
  UNBOOKMARK_POST,
} from "../graphql/mutations/postMutations";

const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK_DATA === "true";

export const usePostInteraction = (postId: string) => {
  const [isLiking, setIsLiking] = useState(false);
  const [isCommenting, setIsCommenting] = useState(false);
  const [isSharing, setIsSharing] = useState(false);
  const [isBookmarking, setIsBookmarking] = useState(false);

  const [likePostMutation] = useMutation(LIKE_POST);
  const [unlikePostMutation] = useMutation(UNLIKE_POST);
  const [addCommentMutation] = useMutation(ADD_COMMENT);
  const [sharePostMutation] = useMutation(SHARE_POST);
  const [bookmarkPostMutation] = useMutation(BOOKMARK_POST);
  const [unbookmarkPostMutation] = useMutation(UNBOOKMARK_POST);

  const toggleLike = useCallback(
    async (isLiked: boolean) => {
      if (USE_MOCK_DATA) {
        setIsLiking(true);
        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 300));
        setIsLiking(false);
        return { success: true };
      }

      setIsLiking(true);
      try {
        if (isLiked) {
          await unlikePostMutation({
            variables: { postId },
            optimisticResponse: {
              unlikePost: {
                __typename: "Post",
                id: postId,
                likes: -1, // This will be handled by the cache
                liked: false,
              },
            },
          });
        } else {
          await likePostMutation({
            variables: { postId },
            optimisticResponse: {
              likePost: {
                __typename: "Post",
                id: postId,
                likes: 1, // This will be handled by the cache
                liked: true,
              },
            },
          });
        }
        return { success: true };
      } catch (error) {
        console.error("Error toggling like:", error);
        return { success: false, error };
      } finally {
        setIsLiking(false);
      }
    },
    [postId, likePostMutation, unlikePostMutation],
  );

  const addComment = useCallback(
    async (text: string, parentId?: string) => {
      if (USE_MOCK_DATA) {
        setIsCommenting(true);
        await new Promise((resolve) => setTimeout(resolve, 500));
        setIsCommenting(false);
        return { success: true };
      }

      setIsCommenting(true);
      try {
        await addCommentMutation({
          variables: { postId, text, parentId },
        });
        return { success: true };
      } catch (error) {
        console.error("Error adding comment:", error);
        return { success: false, error };
      } finally {
        setIsCommenting(false);
      }
    },
    [postId, addCommentMutation],
  );

  const sharePost = useCallback(async () => {
    if (USE_MOCK_DATA) {
      setIsSharing(true);
      await new Promise((resolve) => setTimeout(resolve, 300));
      setIsSharing(false);
      return { success: true };
    }

    setIsSharing(true);
    try {
      await sharePostMutation({
        variables: { postId },
      });
      return { success: true };
    } catch (error) {
      console.error("Error sharing post:", error);
      return { success: false, error };
    } finally {
      setIsSharing(false);
    }
  }, [postId, sharePostMutation]);

  const toggleBookmark = useCallback(
    async (isBookmarked: boolean) => {
      if (USE_MOCK_DATA) {
        setIsBookmarking(true);
        await new Promise((resolve) => setTimeout(resolve, 300));
        setIsBookmarking(false);
        return { success: true };
      }

      setIsBookmarking(true);
      try {
        if (isBookmarked) {
          await unbookmarkPostMutation({
            variables: { postId },
          });
        } else {
          await bookmarkPostMutation({
            variables: { postId },
          });
        }
        return { success: true };
      } catch (error) {
        console.error("Error toggling bookmark:", error);
        return { success: false, error };
      } finally {
        setIsBookmarking(false);
      }
    },
    [postId, bookmarkPostMutation, unbookmarkPostMutation],
  );

  return {
    toggleLike,
    addComment,
    sharePost,
    toggleBookmark,
    isLiking,
    isCommenting,
    isSharing,
    isBookmarking,
  };
};
