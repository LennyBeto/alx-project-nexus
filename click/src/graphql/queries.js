// src/graphql/queries.js
import { gql } from "@apollo/client";

// Authentication queries
export const LOGIN_USER = gql`
  mutation LoginUser($username: String!, $password: String!) {
    loginUser(username: $username, password: $password) {
      success
      message
      token
      user {
        id
        username
        email
        firstName
        lastName
        fullName
      }
    }
  }
`;

export const REGISTER_USER = gql`
  mutation RegisterUser(
    $username: String!
    $email: String!
    $password: String!
    $firstName: String
    $lastName: String
  ) {
    registerUser(
      username: $username
      email: $email
      password: $password
      firstName: $firstName
      lastName: $lastName
    ) {
      success
      message
      token
      user {
        id
        username
        email
        firstName
        lastName
        fullName
      }
    }
  }
`;

export const GET_ME = gql`
  query GetMe {
    me {
      id
      username
      email
      firstName
      lastName
      fullName
      postsCount
      followersCount
      followingCount
    }
  }
`;

// Post queries
export const GET_POSTS = gql`
  query GetPosts($limit: Int, $offset: Int) {
    posts(limit: $limit, offset: $offset) {
      id
      content
      imageUrl
      createdAt
      likesCount
      commentsCount
      sharesCount
      isLikedByUser
      isSharedByUser
      author {
        id
        username
        fullName
      }
    }
  }
`;

export const GET_FEED = gql`
  query GetFeed($limit: Int, $offset: Int) {
    feed(limit: $limit, offset: $offset) {
      id
      content
      imageUrl
      createdAt
      likesCount
      commentsCount
      sharesCount
      isLikedByUser
      isSharedByUser
      author {
        id
        username
        fullName
      }
    }
  }
`;

export const GET_POST_DETAILS = gql`
  query GetPostDetails($postId: Int!) {
    post(id: $postId) {
      id
      content
      imageUrl
      createdAt
      likesCount
      commentsCount
      sharesCount
      isLikedByUser
      isSharedByUser
      author {
        id
        username
        fullName
      }
    }
    comments(postId: $postId) {
      id
      content
      createdAt
      repliesCount
      isLikedByUser
      author {
        id
        username
        fullName
      }
    }
  }
`;

// Post mutations
export const CREATE_POST = gql`
  mutation CreatePost($content: String!, $imageUrl: String) {
    createPost(content: $content, imageUrl: $imageUrl) {
      success
      message
      post {
        id
        content
        imageUrl
        createdAt
        likesCount
        commentsCount
        sharesCount
        author {
          id
          username
          fullName
        }
      }
    }
  }
`;

export const LIKE_POST = gql`
  mutation LikePost($postId: Int!) {
    likePost(postId: $postId) {
      success
      message
    }
  }
`;

export const SHARE_POST = gql`
  mutation SharePost($postId: Int!, $message: String) {
    sharePost(postId: $postId, message: $message) {
      success
      message
    }
  }
`;

export const CREATE_COMMENT = gql`
  mutation CreateComment($postId: Int!, $content: String!, $parentId: Int) {
    createComment(postId: $postId, content: $content, parentId: $parentId) {
      success
      message
      comment {
        id
        content
        createdAt
        author {
          id
          username
          fullName
        }
      }
    }
  }
`;

export const FOLLOW_USER = gql`
  mutation FollowUser($userId: Int!) {
    followUser(userId: $userId) {
      success
      message
    }
  }
`;

// User queries
export const GET_USER_PROFILE = gql`
  query GetUserProfile($userId: Int!) {
    user(id: $userId) {
      id
      username
      fullName
      dateJoined
      postsCount
      followersCount
      followingCount
    }
    posts(authorId: $userId, limit: 20) {
      id
      content
      imageUrl
      createdAt
      likesCount
      commentsCount
      sharesCount
    }
  }
`;

export const SEARCH_POSTS = gql`
  query SearchPosts($search: String!, $limit: Int) {
    posts(search: $search, limit: $limit) {
      id
      content
      createdAt
      likesCount
      commentsCount
      author {
        id
        username
        fullName
      }
    }
  }
`;
