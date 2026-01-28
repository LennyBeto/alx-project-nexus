import React, { useState } from "react";
import { Heart, MessageCircle, Share2, Bookmark } from "lucide-react";
import { Post as PostType } from "../../types";
import { Avatar } from "../UI/Avatar";
import { formatTime, formatCount } from "../../utils/formatTime";
import { usePostInteraction } from "../../hooks/usePostInteraction";
import { CommentSection } from "./CommentSection";
import clsx from "clsx";

interface PostProps {
  post: PostType;
}

export const Post: React.FC<PostProps> = ({ post }) => {
  const [localPost, setLocalPost] = useState(post);
  const [showComments, setShowComments] = useState(false);
  const { toggleLike, sharePost, toggleBookmark, isLiking } =
    usePostInteraction(post.id);

  const handleLike = async () => {
    const newLiked = !localPost.liked;
    const newLikes = newLiked ? localPost.likes + 1 : localPost.likes - 1;

    setLocalPost((prev) => ({
      ...prev,
      liked: newLiked,
      likes: newLikes,
    }));

    const result = await toggleLike(localPost.liked);
    if (!result.success) {
      // Revert on error
      setLocalPost((prev) => ({
        ...prev,
        liked: !newLiked,
        likes: post.likes,
      }));
    }
  };

  const handleBookmark = async () => {
    const newBookmarked = !localPost.bookmarked;
    setLocalPost((prev) => ({
      ...prev,
      bookmarked: newBookmarked,
    }));

    const result = await toggleBookmark(localPost.bookmarked || false);
    if (!result.success) {
      setLocalPost((prev) => ({
        ...prev,
        bookmarked: !newBookmarked,
      }));
    }
  };

  const handleShare = async () => {
    await sharePost();
    if (navigator.share) {
      navigator.share({
        title: `Post by ${post.user.name}`,
        text: post.content,
        url: window.location.href,
      });
    }
  };

  return (
    <article className="bg-white rounded-lg shadow-card hover:shadow-card-hover transition-shadow duration-300 mb-4 animate-fade-in">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start space-x-3">
          <Avatar
            src={localPost.user.avatar}
            alt={localPost.user.name}
            size="md"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <h3 className="font-semibold text-dark-900 truncate">
                {localPost.user.name}
              </h3>
              {localPost.user.verified && (
                <svg
                  className="w-4 h-4 text-primary-600"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </div>
            <div className="flex items-center space-x-2 text-sm text-dark-500">
              <span>@{localPost.user.username}</span>
              <span>·</span>
              <time dateTime={localPost.timestamp}>
                {formatTime(localPost.timestamp)}
              </time>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="mt-4">
          <p className="text-dark-900 whitespace-pre-wrap">
            {localPost.content}
          </p>

          {localPost.imageUrl && (
            <div className="mt-4 rounded-lg overflow-hidden">
              <img
                src={localPost.imageUrl}
                alt="Post content"
                className="w-full h-auto object-cover max-h-96"
                loading="lazy"
              />
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-dark-100">
          <button
            onClick={handleLike}
            disabled={isLiking}
            className={clsx(
              "flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200",
              localPost.liked
                ? "text-red-600 bg-red-50 hover:bg-red-100"
                : "text-dark-600 hover:bg-dark-50",
            )}
          >
            <Heart
              className={clsx(
                "w-5 h-5 transition-transform duration-200",
                localPost.liked && "fill-current scale-110",
              )}
            />
            <span className="font-medium text-sm">
              {formatCount(localPost.likes)}
            </span>
          </button>

          <button
            onClick={() => setShowComments(!showComments)}
            className="flex items-center space-x-2 px-3 py-2 rounded-lg text-dark-600 hover:bg-dark-50 transition-all duration-200"
          >
            <MessageCircle className="w-5 h-5" />
            <span className="font-medium text-sm">
              {formatCount(
                localPost.commentsCount || localPost.comments.length,
              )}
            </span>
          </button>

          <button
            onClick={handleShare}
            className="flex items-center space-x-2 px-3 py-2 rounded-lg text-dark-600 hover:bg-dark-50 transition-all duration-200"
          >
            <Share2 className="w-5 h-5" />
            <span className="font-medium text-sm">
              {formatCount(localPost.shares)}
            </span>
          </button>

          <button
            onClick={handleBookmark}
            className={clsx(
              "p-2 rounded-lg transition-all duration-200",
              localPost.bookmarked
                ? "text-primary-600 bg-primary-50"
                : "text-dark-600 hover:bg-dark-50",
            )}
          >
            <Bookmark
              className={clsx(
                "w-5 h-5",
                localPost.bookmarked && "fill-current",
              )}
            />
          </button>
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="border-t border-dark-100">
          <CommentSection postId={localPost.id} comments={localPost.comments} />
        </div>
      )}
    </article>
  );
};
