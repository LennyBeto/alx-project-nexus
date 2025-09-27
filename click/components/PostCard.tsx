import { useState } from "react";
import { View, Text, TouchableOpacity, Modal, TextInput, FlatList } from "react-native";
import { FontAwesome6, SimpleLineIcons } from "@expo/vector-icons";
import { PostProps } from "@/interfaces";
import { styles } from "@/styles/_poststyles";

export default function PostCard({ post }: PostProps) {
  const [likes, setlikes] = useState(post.likes);
  const [comments, setComments] = useState(post.comments);
  const [shares, setShares] = useState(post.shares);
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [showRepostModal, setShowRepostModal] = useState(false);
  const [thought, setThought] = useState("");

  const handleLike = () => setlikes((prev) => prev + 1);
  
  const handleAddComment = () => {
    if (!newComment.trim()) return;

    const comment = {
      id: String(comments.length + 1),
      Author: "CurrentUser",
      text: newComment,
      CreatedAt: new Date().toISOString(),
    };
    setComments((prev) => [...prev, comment]);
    setNewComment("");
  };

  const handleRepost = (withThought: boolean) => {
    setShowRepostModal(false);
    setShares((prev) => prev + 1);

    // TODO: send to backend (supabase/firebase) here
    console.log("Reposted:", {
      postId: post.id,
      thought: withThought ? thought : null,
      user: "CurrentUser", // replace with auth user
    });

    setThought(""); // reset
  };

  return (
    <View style={styles.card}>
      <Text style={styles.author}>{post.author}</Text>
      <Text style={styles.content}>{post.content}</Text>
      <Text style={styles.date}>
        {new Date(post.createdAt).toLocaleString()}
      </Text>

      <View style={styles.actions}>
        <TouchableOpacity style={styles.button} onPress={handleLike}>
          <SimpleLineIcons name="like" size={15} color="red" />
          <Text style={{ color: "white" }}>{likes}</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => setShowComments(true)}>
          <FontAwesome6 name="commenting" size={15} color="blue" />
          <Text style={{ color: "white", marginLeft: 6 }}>
            {comments.length}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => setShowRepostModal(true)}>
          <FontAwesome6 name="share" size={15} color="green" />
          <Text style={{ color: "white", marginLeft: 6 }}>{shares}</Text>
        </TouchableOpacity>
      </View>
      <Modal visible={showComments} animationType="slide">
        <View style={styles.modal}>
          <Text style={styles.modalTitle}>Comments</Text>

          <FlatList
            data={comments}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <View style={styles.commentRow}>
                <Text style={styles.commentAuthor}>{item.author}:</Text>
                <Text style={styles.commentText}>{item.text}</Text>
              </View>
            )}
          />

          <View style={styles.inputRow}>
            <TextInput
              style={styles.input}
              value={newComment}
              onChangeText={setNewComment}
              placeholder="Write a comment..."
              placeholderTextColor="gray"
            />
            <TouchableOpacity onPress={handleAddComment}>
              <Text style={styles.addButton}>Post</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity onPress={() => setShowComments(false)}>
            <Text style={styles.closeBtn}>Close</Text>
          </TouchableOpacity>
        </View>
      </Modal>

      <Modal visible={showRepostModal} animationType="slide" transparent>
        <View style={styles.overlay}>
          <View style={styles.repostBox}>
            <Text style={styles.modalTitle}>Repost Options</Text>

            <TextInput
              style={styles.input}
              placeholder="Add your thoughts (optional)"
              placeholderTextColor="gray"
              value={thought}
              onChangeText={setThought}
            />

            <TouchableOpacity
              style={styles.modalBtn}
              onPress={() => handleRepost(false)}
            >
              <Text style={styles.btnText}>Repost Without Thought</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.modalBtn}
              onPress={() => handleRepost(true)}
            >
              <Text style={styles.btnText}>Repost With Thought</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => setShowRepostModal(false)}>
              <Text style={styles.closeBtn}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

    </View>
  );
}

