import React, { useEffect } from "react";
import { Post } from "./Post";
import { PostSkeleton } from "./PostSkeleton";
import { Loader } from "../UI/Loader";
import { usePosts } from "../../hooks/usePosts";
import { useInfiniteScroll } from "../../hooks/useInfiniteScroll";
import { RefreshCw } from "lucide-react";

export const Feed: React.FC = () => {
  const { posts, loading, error, hasMore, loadMore, refresh } = usePosts();
  const { loadMoreRef } = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    isLoading: loading,
  });

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">
          Error loading posts. Please try again.
        </p>
        <button
          onClick={refresh}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <RefreshCw className="w-4 h-4 inline mr-2" />
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-dark-900">Feed</h1>
        <button
          onClick={refresh}
          className="p-2 rounded-lg hover:bg-dark-100 transition-colors"
          aria-label="Refresh feed"
        >
          <RefreshCw className="w-5 h-5 text-dark-600" />
        </button>
      </div>

      {/* Posts */}
      {loading && posts.length === 0 ? (
        <>
          <PostSkeleton />
          <PostSkeleton />
          <PostSkeleton />
        </>
      ) : (
        <>
          {posts.map((post) => (
            <Post key={post.id} post={post} />
          ))}

          {/* Load More Trigger */}
          {hasMore && (
            <div ref={loadMoreRef} className="py-4">
              <Loader />
            </div>
          )}

          {!hasMore && posts.length > 0 && (
            <p className="text-center text-dark-500 py-8">
              You've reached the end! 🎉
            </p>
          )}
        </>
      )}
    </div>
  );
};
