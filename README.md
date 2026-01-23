
# Dynamic Social Media Feed

<div align="center">

![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178C6?style=for-the-badge&logo=typescript)
![GraphQL](https://img.shields.io/badge/GraphQL-16.8.1-E10098?style=for-the-badge&logo=graphql)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.0-06B6D4?style=for-the-badge&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A modern, production-ready social media feed application with real-time interactions**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## Overview

The **Dynamic Social Media Feed** is a modern, responsive web application that replicates core social media functionality. Built with React, TypeScript, and GraphQL, it provides users with an engaging platform to view, interact with, and share content in real-time.

### Real-World Application

This project mirrors production-grade social media platforms by implementing:
- **Efficient Data Fetching**: GraphQL for optimized API queries
- **Real-Time Interactions**: Instant feedback on likes, comments, and shares
- **Infinite Scrolling**: Seamless content loading as users scroll
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Type Safety**: Full TypeScript implementation for robust code

---

## Features

### Core Functionality

#### 🔄 Dynamic Post Loading
- GraphQL-powered data fetching
- Infinite scroll with pagination
- Optimistic UI updates
- Loading states and skeleton screens
- Error handling and retry logic

#### User Interactions
- **Like Posts**: Real-time like counter updates with optimistic UI
- **Comment**: Threaded comment system with instant feedback
- **Share**: Social sharing functionality
- **Bookmark**: Save posts for later

#### Enhanced User Experience
- Smooth animations and transitions
- Responsive design (mobile-first approach)
- Dark mode support (coming soon)
- Accessibility (WCAG 2.1 AA compliant)
- Progressive Web App (PWA) capabilities

#### Performance Features
- Code splitting and lazy loading
- Image optimization and lazy loading
- Debounced search and interactions
- Memoization for expensive operations
- Service Worker for offline support

---

## Tech Stack

### Frontend
- **React 18.2.0** - UI library with concurrent features
- **TypeScript 5.3.3** - Type safety and better DX
- **React Router 6.20.1** - Client-side routing
- **Tailwind CSS 3.4.0** - Utility-first CSS framework

### State Management & Data Fetching
- **Apollo Client 3.8.8** - GraphQL client with caching
- **GraphQL 16.8.1** - Query language for APIs

### UI Components & Icons
- **Lucide React** - Beautiful, consistent icons
- **clsx** - Utility for constructing className strings

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Husky** - Git hooks
- **lint-staged** - Run linters on staged files

### Testing
- **Jest** - Testing framework
- **React Testing Library** - Component testing
- **@testing-library/user-event** - User interaction testing

---

## Architecture

### Component Architecture

```
┌─────────────────────────────────────┐
│           App Component             │
│     (Apollo Provider Wrapper)       │
└────────────┬────────────────────────┘
             │
    ┌────────▼────────┐
    │   Feed Container │
    │  (Data Fetching) │
    └────────┬─────────┘
             │
    ┌────────▼─────────────────────────┐
    │         Post List                │
    │    (Infinite Scroll)             │
    └────────┬─────────────────────────┘
             │
    ┌────────▼──────────┐
    │   Post Component   │
    │  (User Actions)    │
    └────────┬───────────┘
             │
    ┌────────▼──────────┐
    │ Comment Section    │
    │ (Nested Comments)  │
    └────────────────────┘
```

### Data Flow

```
User Action
    ↓
Component Handler
    ↓
GraphQL Mutation/Query
    ↓
Apollo Client (Cache Update)
    ↓
Component Re-render
    ↓
UI Update
```

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js** >= 18.0.0 ([Download](https://nodejs.org/))
- **npm** >= 9.0.0 or **yarn** >= 1.22.0
- **Git** ([Download](https://git-scm.com/))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/social-media-feed.git
cd social-media-feed
```

2. **Install dependencies**

```bash
npm install
# or
yarn install
```

3. **Set up environment variables**

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your configuration:

```env
REACT_APP_GRAPHQL_ENDPOINT=https://your-api.com/graphql
REACT_APP_API_KEY=your_api_key_here
REACT_APP_ENV=development
```

### Environment Setup

#### GraphQL Backend Setup (Optional)

If you don't have a GraphQL backend, you can use the mock data mode:

```env
REACT_APP_USE_MOCK_DATA=true
```

Or set up a quick GraphQL server using our backend template:

```bash
git clone https://github.com/LennyBeto/social-feed-backend.git
cd social-feed-backend
npm install
npm start
```

### Running the App

#### Development Mode

```bash
npm start
```

Opens [http://localhost:3000](http://localhost:3000) in your browser.

#### Production Build

```bash
npm run build
```

Builds the app for production to the `build` folder.

#### Testing

```bash
# Run tests in watch mode
npm test

# Run tests with coverage
npm run test:coverage
```

---

## 📁 Project Structure

```
social-media-feed/
├── public/                 # Static files
│   ├── index.html         # HTML template
│   ├── manifest.json      # PWA manifest
│   └── robots.txt         # SEO robots file
│
├── src/
│   ├── components/        # React components
│   │   ├── Feed/         # Feed-related components
│   │   │   ├── Post.tsx              # Individual post
│   │   │   ├── PostSkeleton.tsx      # Loading skeleton
│   │   │   ├── CommentSection.tsx    # Comments UI
│   │   │   └── index.ts              # Barrel export
│   │   │
│   │   ├── UI/           # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Avatar.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Loader.tsx
│   │   │
│   │   └── Layout/       # Layout components
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── Container.tsx
│   │
│   ├── graphql/          # GraphQL configuration
│   │   ├── client.ts             # Apollo Client setup
│   │   ├── queries/              # GraphQL queries
│   │   │   ├── getPosts.ts
│   │   │   └── getComments.ts
│   │   └── mutations/            # GraphQL mutations
│   │       ├── likePost.ts
│   │       ├── addComment.ts
│   │       └── sharePost.ts
│   │
│   ├── hooks/            # Custom React hooks
│   │   ├── usePosts.ts           # Posts data management
│   │   ├── useInfiniteScroll.ts  # Infinite scroll logic
│   │   ├── useInteraction.ts     # User interactions
│   │   └── useDebounce.ts        # Debounce utility
│   │
│   ├── types/            # TypeScript types
│   │   ├── post.ts
│   │   ├── user.ts
│   │   └── comment.ts
│   │
│   ├── utils/            # Utility functions
│   │   ├── formatTime.ts         # Time formatting
│   │   ├── storage.ts            # Local storage wrapper
│   │   └── constants.ts          # App constants
│   │
│   ├── styles/           # Global styles
│   │   ├── global.css
│   │   └── animations.css
│   │
│   ├── App.tsx           # Root component
│   ├── index.tsx         # Entry point
│   └── react-app-env.d.ts
│
├── .github/
│   └── workflows/        # GitHub Actions
│       └── ci-cd.yml
│
├── .env.example          # Environment variables template
├── .gitignore
├── .eslintrc.json        # ESLint configuration
├── .prettierrc           # Prettier configuration
├── tsconfig.json         # TypeScript configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── package.json
├── README.md             # This file
└── DEPLOYMENT.md         # Deployment guide
```

---

## Development

### Code Style

This project uses ESLint and Prettier for code consistency:

```bash
# Run linter
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

### Git Workflow

We follow conventional commits for clear commit history:

```bash
# Feature
git commit -m "feat: add user profile component"

# Bug fix
git commit -m "fix: resolve infinite scroll issue"

# Style changes
git commit -m "style: improve post card layout"

# Documentation
git commit -m "docs: update API integration guide"

# Performance
git commit -m "perf: optimize image loading"
```

### Pre-commit Hooks

Husky and lint-staged run automatically before commits:
- Lints staged files
- Formats code
- Runs type checking

---

## Testing

### Running Tests

```bash
# Watch mode
npm test

# Coverage report
npm run test:coverage

# CI mode
npm run test:ci
```

### Test Structure

```typescript
// Example test
import { render, screen, fireEvent } from '@testing-library/react';
import Post from './Post';

describe('Post Component', () => {
  it('renders post content', () => {
    render(<Post {...mockPost} />);
    expect(screen.getByText(mockPost.content)).toBeInTheDocument();
  });

  it('handles like interaction', () => {
    const onLike = jest.fn();
    render(<Post {...mockPost} onLike={onLike} />);
    
    fireEvent.click(screen.getByRole('button', { name: /like/i }));
    expect(onLike).toHaveBeenCalledWith(mockPost.id);
  });
});
```

### Coverage Goals

- **Statements**: > 80%
- **Branches**: > 75%
- **Functions**: > 80%
- **Lines**: > 80%

---

## 🚀 Deployment

### Deployment Options

#### 1. Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or use the GitHub integration for automatic deployments.

#### 2. Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Build and deploy
npm run build
netlify deploy --prod --dir=build
```

#### 3. AWS Amplify

```bash
# Install Amplify CLI
npm i -g @aws-amplify/cli

# Initialize and deploy
amplify init
amplify add hosting
amplify publish
```

#### 4. Docker

```dockerfile
# Dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# Build and run
docker build -t social-feed .
docker run -p 80:80 social-feed
```

### Environment Variables for Production

```env
REACT_APP_GRAPHQL_ENDPOINT=https://api.production.com/graphql
REACT_APP_API_KEY=prod_api_key
REACT_APP_ENV=production
REACT_APP_ANALYTICS_ID=your_analytics_id
```

---

## API Integration

### GraphQL Schema Example

```graphql
type User {
  id: ID!
  name: String!
  username: String!
  avatar: String!
  verified: Boolean
}

type Comment {
  id: ID!
  user: User!
  text: String!
  timestamp: String!
  likes: Int!
}

type Post {
  id: ID!
  user: User!
  content: String!
  imageUrl: String
  likes: Int!
  comments: [Comment!]!
  shares: Int!
  timestamp: String!
  liked: Boolean!
}

type PostsResponse {
  posts: [Post!]!
  hasMore: Boolean!
  nextCursor: String
}

type Query {
  posts(limit: Int!, cursor: String): PostsResponse!
  post(id: ID!): Post
}

type Mutation {
  likePost(postId: ID!): Post!
  unlikePost(postId: ID!): Post!
  addComment(postId: ID!, text: String!): Post!
  sharePost(postId: ID!): Post!
}
```

### Making API Calls

```typescript
// Query example
const { data, loading } = useQuery(GET_POSTS, {
  variables: { limit: 10, cursor: null },
});

// Mutation example
const [likePost] = useMutation(LIKE_POST, {
  onCompleted: (data) => {
    console.log('Post liked:', data);
  },
});
```

---

## Performance Optimization

### Implemented Optimizations

1. **Code Splitting**
   ```typescript
   const Profile = lazy(() => import('./components/Profile'));
   ```

2. **Image Optimization**
   - Lazy loading images
   - Responsive images with srcset
   - WebP format support

3. **Memoization**
   ```typescript
   const MemoizedPost = React.memo(Post, (prev, next) => {
     return prev.post.id === next.post.id && 
            prev.post.likes === next.post.likes;
   });
   ```

4. **Virtual Scrolling** (for large lists)
   ```typescript
   import { FixedSizeList } from 'react-window';
   ```

5. **Apollo Client Caching**
   - Normalized cache
   - Cache-first policies
   - Optimistic updates

### Performance Metrics

- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Lighthouse Score**: > 90

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow the existing code style
- Update documentation as needed
- Ensure all tests pass
- Add meaningful commit messages

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [React Documentation](https://react.dev/)
- [Apollo GraphQL](https://www.apollographql.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

---

## Support

-  Email: lennybeto.lb@gmail.com
-  Issues: [GitHub Issues](https://github.com/LennyBeto/social-media-feed/issues)

---

## Roadmap

- [ ] Dark mode support
- [ ] Real-time notifications
- [ ] Video post support
- [ ] Story feature
- [ ] Advanced search and filters
- [ ] User profiles
- [ ] Direct messaging
- [ ] Mobile app (React Native)

---

<div align="center">

**Made with ❤️ by Lenny Beto**

⭐ Star us on GitHub — it helps!

[Report Bug](https://github.com/LennyBeto/social-media-feed/issues) • [Request Feature](https://github.com/LennyBeto/social-media-feed/issues)

</div>
