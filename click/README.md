# 📸 Click  

**Click** is a simple social media platform built around **viewing and engaging with posts**.  
It’s not a place for endless chatting or distractions — just a space where you can:  

- **View posts**  
- **Like posts**  
- **Comment on posts**  
- **Repost (share) posts**  
- **Add your own posts**  
- **Get notifications** about engagement  

That’s it. Clean, minimal, and user-first.  

---

## 🚀 Why Click?  

Most social media platforms try to be everything at once — messaging, shopping, livestreaming, and more.  
**Click strips away the noise and focuses only on the essentials**: engaging with posts.  

👉 Think of it as a place to **scroll, react, and share content without distraction.**  

---

## ✨ Core Features (MVP)  

- **Post Feed** – Browse through posts in a distraction-free timeline.  
- **Like** – React instantly with a tap.  
- **Comment** – Add your thoughts to a post.  
- **Repost (Share)** – Amplify posts you enjoy.  
- **Add Post** – Share your own content with the feed.  
- **Notifications** – Stay updated on likes, comments, and reposts.  

---

## ⚙️ Tech Stack  

- **React Native** – Core framework for building the app.  
- **Expo + NativeWind** – Styling and component management.  
- **GraphQL** – For fetching and displaying posts.  

> 📝 Note: No backend was used for this MVP.  

---

## 📱 Usage Flow  

1. **Landing Page** – Welcome screen introducing the app.  
2. **Sign Up / Log In** – Create an account or log in.  
3. **Home Feed** – Scroll through posts and engage (like, comment, repost).  
4. **Profile** – View your activity and shared posts.  
5. **Notifications** – See who engaged with your content.  
6. **Add Post** – Create and share your own posts.  
7. **Logout** – Exit securely from the app.  

---

## 🛠️ Getting Started  

Follow these steps to run **Click** locally:  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/click.git
   cd click
2. **Install dependencies**
   ```bash
   npm install

3. **Start the development server**
   ```bash
   npx expo start

Open the project on Expo Go (iOS/Android) or run on an emulator.

## 👩‍💻 Contribution Guidelines

We welcome contributions! Here’s how you can help:

1. Fork the repository.
   
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   
3. Commit your changes:
   ```bash
   git commit -m "Add: short description of your feature"
   
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name

5. Submit a Pull Request for review.

## 📌 Vision

Click is built to bring back the simplicity of early social media — a space to share and engage with content without endless features. Future versions may expand based on feedback, but the core will always remain simple and engagement-focused.

## 🐛 Known Issues

- Limited offline support (requires internet to fetch posts).

- Notifications may not update in real time.

- No backend storage — posts reset if the app is restarted.

- MVP design — some screens may look minimal until further improvements.
