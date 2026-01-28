// graphql/queries/getPosts.ts

import { gql } from "@apollo/client";

export const GET_POSTS = gql`
  query GetPosts($limit: Int!, $cursor: String) {
    posts(limit: $limit, cursor: $cursor) {
      posts {
        id
        user {
          id
          name
          username
          avatar
          verified
        }
        content
        imageUrl
        likes
        commentsCount
        shares
        timestamp
        liked
        bookmarked
      }
      hasMore
      nextCursor
    }
  }
`;

export const GET_POST = gql`
  query GetPost($id: ID!) {
    post(id: $id) {
      id
      user {
        id
        name
        username
        avatar
        verified
      }
      content
      imageUrl
      videoUrl
      likes
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
      shares
      timestamp
      liked
      bookmarked
    }
  }
`;
