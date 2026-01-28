// utils/mockData.ts

import { Post, User } from "../types";

export const mockUsers: User[] = [
  {
    id: "1",
    name: "Sarah Johnson",
    username: "sarahj",
    avatar: "https://i.pravatar.cc/150?img=1",
    verified: true,
  },
  {
    id: "2",
    name: "Mike Chen",
    username: "mikechen",
    avatar: "https://i.pravatar.cc/150?img=2",
    verified: false,
  },
  {
    id: "3",
    name: "Emma Williams",
    username: "emmaw",
    avatar: "https://i.pravatar.cc/150?img=3",
    verified: true,
  },
  {
    id: "4",
    name: "James Brown",
    username: "jbrown",
    avatar: "https://i.pravatar.cc/150?img=4",
    verified: false,
  },
];

export const mockPosts: Post[] = [
  {
    id: "1",
    user: mockUsers[0],
    content:
      "Just launched our new product! 🚀 Excited to share this journey with all of you. Check it out and let me know what you think! #ProductLaunch #Innovation",
    imageUrl:
      "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=600&fit=crop",
    likes: 1245,
    commentsCount: 87,
    shares: 43,
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    liked: false,
    bookmarked: false,
    comments: [
      {
        id: "c1",
        user: mockUsers[1],
        text: "Congratulations! This looks amazing! 🎉",
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        likes: 23,
        liked: false,
      },
      {
        id: "c2",
        user: mockUsers[2],
        text: "Been waiting for this! When can we try it out?",
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        likes: 12,
        liked: true,
      },
    ],
  },
  {
    id: "2",
    user: mockUsers[1],
    content:
      "Beautiful sunrise this morning 🌅 Sometimes you just need to pause and appreciate the little things in life. What made you smile today?",
    imageUrl:
      "https://images.unsplash.com/photo-1495344517868-8ebaf0a2044a?w=800&h=600&fit=crop",
    likes: 892,
    commentsCount: 45,
    shares: 21,
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    liked: true,
    bookmarked: true,
    comments: [
      {
        id: "c3",
        user: mockUsers[3],
        text: "Stunning photo! Where was this taken?",
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
        likes: 8,
        liked: false,
      },
    ],
  },
  {
    id: "3",
    user: mockUsers[2],
    content:
      "Hot take: TypeScript makes JavaScript development so much better. Who agrees? 💙 #WebDev #TypeScript #JavaScript",
    likes: 2341,
    commentsCount: 156,
    shares: 89,
    timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
    liked: false,
    bookmarked: false,
    comments: [
      {
        id: "c4",
        user: mockUsers[0],
        text: "Absolutely! Type safety is a game changer.",
        timestamp: new Date(Date.now() - 7 * 60 * 60 * 1000).toISOString(),
        likes: 45,
        liked: true,
      },
      {
        id: "c5",
        user: mockUsers[3],
        text: "I was skeptical at first, but now I can't imagine going back!",
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
        likes: 32,
        liked: false,
      },
    ],
  },
  {
    id: "4",
    user: mockUsers[3],
    content:
      "Working on an exciting new feature for our app. Can't wait to show you all what we've been building! Stay tuned... 👀",
    likes: 567,
    commentsCount: 34,
    shares: 12,
    timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    liked: false,
    bookmarked: false,
    comments: [],
  },
  {
    id: "5",
    user: mockUsers[0],
    content:
      "Reminder: Take breaks, drink water, and don't forget to stretch! Your body will thank you 💪 #HealthyHabits #Wellness",
    imageUrl:
      "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop",
    likes: 1876,
    commentsCount: 92,
    shares: 156,
    timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    liked: true,
    bookmarked: true,
    comments: [
      {
        id: "c6",
        user: mockUsers[1],
        text: "Thanks for the reminder! Just took a quick stretch break 😊",
        timestamp: new Date(Date.now() - 23 * 60 * 60 * 1000).toISOString(),
        likes: 15,
        liked: false,
      },
    ],
  },
];

export const generateMorePosts = (count: number, startId: number): Post[] => {
  const posts: Post[] = [];

  for (let i = 0; i < count; i++) {
    const user = mockUsers[Math.floor(Math.random() * mockUsers.length)];
    const hoursAgo = Math.floor(Math.random() * 72) + 1;

    posts.push({
      id: (startId + i).toString(),
      user,
      content: `This is post number ${startId + i}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. #Post${startId + i}`,
      imageUrl:
        Math.random() > 0.5
          ? `https://images.unsplash.com/photo-${1500000000000 + Math.floor(Math.random() * 100000000)}?w=800&h=600&fit=crop`
          : undefined,
      likes: Math.floor(Math.random() * 5000),
      commentsCount: Math.floor(Math.random() * 200),
      shares: Math.floor(Math.random() * 100),
      timestamp: new Date(Date.now() - hoursAgo * 60 * 60 * 1000).toISOString(),
      liked: Math.random() > 0.7,
      bookmarked: Math.random() > 0.8,
      comments: [],
    });
  }

  return posts;
};
