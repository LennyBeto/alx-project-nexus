// graphql/mutations/postMutations.ts

import { gql } from "@apollo/client";

export const LIKE_POST = gql`
  mutation LikePost($postId: ID!) {
    likePost(postId: $postId) {
      id
      likes
      liked
    }
  }
`;

export const UNLIKE_POST = gql`
  mutation UnlikePost($postId: ID!) {
    unlikePost(postId: $postId) {
      id
      likes
      liked
    }
  }
`;

export const ADD_COMMENT = gql`
  mutation AddComment($postId: ID!, $text: String!, $parentId: ID) {
    addComment(postId: $postId, text: $text, parentId: $parentId) {
      id
      comments {
        id
        user {
          id
          name
          username
          avatar
          verified
        }
        text
        timestamp
        likes
        liked
        replies {
          id
          user {
            id
            name
            username
            avatar
            verified
          }
          text
          timestamp
          likes
          liked
        }
      }
      commentsCount
    }
  }
`;

export const SHARE_POST = gql`
  mutation SharePost($postId: ID!) {
    sharePost(postId: $postId) {
      id
      shares
    }
  }
`;

export const BOOKMARK_POST = gql`
  mutation BookmarkPost($postId: ID!) {
    bookmarkPost(postId: $postId) {
      id
      bookmarked
    }
  }
`;

export const UNBOOKMARK_POST = gql`
  mutation UnbookmarkPost($postId: ID!) {
    unbookmarkPost(postId: $postId) {
      id
      bookmarked
    }
  }
`;

export const LIKE_COMMENT = gql`
  mutation LikeComment($commentId: ID!) {
    likeComment(commentId: $commentId) {
      id
      likes
      liked
    }
  }
`;
