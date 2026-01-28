// types/post.ts

import { User } from "./user";
import { Comment } from "./comment";

export interface Post {
  id: string;
  user: User;
  content: string;
  imageUrl?: string;
  videoUrl?: string;
  likes: number;
  comments: Comment[];
  shares: number;
  timestamp: string;
  liked: boolean;
  bookmarked?: boolean;
  commentsCount?: number;
}

export interface PostsResponse {
  posts: Post[];
  hasMore: boolean;
  nextCursor?: string;
}

export interface PostInteraction {
  postId: string;
  action: "like" | "unlike" | "bookmark" | "unbookmark" | "share";
}

export interface PostFilter {
  limit?: number;
  cursor?: string;
  userId?: string;
  hashtag?: string;
}
