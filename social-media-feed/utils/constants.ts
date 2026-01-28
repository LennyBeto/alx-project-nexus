//utils/constants.ts

export const APP_NAME = "Social Media Feed";

export const POSTS_PER_PAGE = 10;

export const MAX_COMMENT_LENGTH = 500;

export const MAX_POST_LENGTH = 280;

export const DEBOUNCE_DELAY = 300;

export const ROUTES = {
  HOME: "/",
  POST: "/post/:id",
  PROFILE: "/profile/:username",
  NOTIFICATIONS: "/notifications",
  MESSAGES: "/messages",
} as const;

export const ANIMATION_DURATION = {
  SHORT: 200,
  MEDIUM: 300,
  LONG: 500,
} as const;

export const ERROR_MESSAGES = {
  NETWORK_ERROR: "Network error. Please check your connection.",
  GENERIC_ERROR: "Something went wrong. Please try again.",
  POST_NOT_FOUND: "Post not found.",
  UNAUTHORIZED: "You need to be logged in to perform this action.",
} as const;

export const SUCCESS_MESSAGES = {
  POST_LIKED: "Post liked!",
  POST_UNLIKED: "Post unliked.",
  COMMENT_ADDED: "Comment added successfully!",
  POST_SHARED: "Post shared!",
  POST_BOOKMARKED: "Post saved to bookmarks.",
} as const;
