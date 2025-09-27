export type Post = {
  id: string;
  author: string;
  content: string;
  createdAt: string;
  likes: number;
  comments: comment[],
  shares: number;
};

export type comment = {
  id: string;
  author: string;
  text: string;
  createdAt: string;
};


export type PostProps = {
  post: Post;
};