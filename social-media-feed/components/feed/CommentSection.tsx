import React, { useState } from "react";
import { Send, Heart } from "lucide-react";
import { Comment } from "../../types";
import { Avatar } from "../UI/Avatar";
import { Button } from "../UI/Button";
import { formatTime } from "../../utils/formatTime";
import { usePostInteraction } from "../../hooks/usePostInteraction";

interface CommentSectionProps {
  postId: string;
  comments: Comment[];
}

export const CommentSection: React.FC<CommentSectionProps> = ({
  postId,
  comments,
}) => {
  const [commentText, setCommentText] = useState("");
  const { addComment, isCommenting } = usePostInteraction(postId);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    const result = await addComment(commentText);
    if (result.success) {
      setCommentText("");
    }
  };

  return (
    <div className="p-6">
      {/* Comment Input */}
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex items-start space-x-3">
          <Avatar src="https://i.pravatar.cc/150?img=0" alt="You" size="sm" />
          <div className="flex-1">
            <textarea
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="Write a comment..."
              className="w-full px-4 py-2 border border-dark-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows={2}
            />
            <div className="mt-2 flex justify-end">
              <Button
                type="submit"
                variant="primary"
                size="sm"
                isLoading={isCommenting}
                disabled={!commentText.trim()}
              >
                <Send className="w-4 h-4 mr-2" />
                Comment
              </Button>
            </div>
          </div>
        </div>
      </form>

      {/* Comments List */}
      <div className="space-y-4">
        {comments.map((comment) => (
          <div
            key={comment.id}
            className="flex items-start space-x-3 animate-slide-up"
          >
            <Avatar
              src={comment.user.avatar}
              alt={comment.user.name}
              size="sm"
            />
            <div className="flex-1">
              <div className="bg-dark-50 rounded-lg p-3">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-sm text-dark-900">
                    {comment.user.name}
                  </span>
                  <span className="text-xs text-dark-500">
                    {formatTime(comment.timestamp)}
                  </span>
                </div>
                <p className="text-dark-800 text-sm mt-1">{comment.text}</p>
              </div>
              <div className="flex items-center space-x-4 mt-2 ml-3">
                <button className="flex items-center space-x-1 text-dark-500 hover:text-red-600 transition-colors text-xs">
                  <Heart className="w-3 h-3" />
                  <span>{comment.likes > 0 && comment.likes}</span>
                </button>
                <button className="text-dark-500 hover:text-primary-600 transition-colors text-xs font-medium">
                  Reply
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
