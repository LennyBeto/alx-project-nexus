// hooks/usePosts.ts

import { useState, useCallback } from "react";
import { useQuery } from "@apollo/client";
import { GET_POSTS } from "../graphql/queries/getPosts";
import { Post, PostsResponse } from "../types";
import { POSTS_PER_PAGE } from "../utils/constants";
import { mockPosts, generateMorePosts } from "../utils/mockData";

const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK_DATA === "true";

export const usePosts = () => {
  const [cursor, setCursor] = useState<string | null>(null);
  const [allPosts, setAllPosts] = useState<Post[]>([]);

  // Mock data implementation
  const [mockData, setMockData] = useState<PostsResponse>(() => ({
    posts: mockPosts,
    hasMore: true,
    nextCursor: "5",
  }));

  const { data, loading, error, fetchMore, refetch } = useQuery<{
    posts: PostsResponse;
  }>(GET_POSTS, {
    variables: { limit: POSTS_PER_PAGE, cursor: null },
    skip: USE_MOCK_DATA,
    notifyOnNetworkStatusChange: true,
    onCompleted: (data) => {
      if (data?.posts?.posts) {
        setAllPosts(data.posts.posts);
      }
    },
  });

  const loadMore = useCallback(() => {
    if (USE_MOCK_DATA) {
      // Mock data pagination
      const currentId = parseInt(mockData.nextCursor || "0");
      const newPosts = generateMorePosts(POSTS_PER_PAGE, currentId);

      setMockData((prev) => ({
        posts: [...prev.posts, ...newPosts],
        hasMore: currentId < 50, // Limit to 50 posts for demo
        nextCursor: (currentId + POSTS_PER_PAGE).toString(),
      }));
    } else {
      // Real API pagination
      if (data?.posts?.nextCursor) {
        fetchMore({
          variables: {
            cursor: data.posts.nextCursor,
          },
          updateQuery: (prev, { fetchMoreResult }) => {
            if (!fetchMoreResult) return prev;

            return {
              posts: {
                ...fetchMoreResult.posts,
                posts: [...prev.posts.posts, ...fetchMoreResult.posts.posts],
              },
            };
          },
        });
      }
    }
  }, [USE_MOCK_DATA, mockData, data, fetchMore]);

  const refresh = useCallback(async () => {
    if (USE_MOCK_DATA) {
      setMockData({
        posts: mockPosts,
        hasMore: true,
        nextCursor: "5",
      });
    } else {
      await refetch({ limit: POSTS_PER_PAGE, cursor: null });
    }
  }, [USE_MOCK_DATA, refetch]);

  if (USE_MOCK_DATA) {
    return {
      posts: mockData.posts,
      loading: false,
      error: null,
      hasMore: mockData.hasMore,
      loadMore,
      refresh,
    };
  }

  return {
    posts: data?.posts?.posts || [],
    loading,
    error,
    hasMore: data?.posts?.hasMore || false,
    loadMore,
    refresh,
  };
};
