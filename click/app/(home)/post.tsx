import React, { useState } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function AddPost() {
  const [content, setContent] = useState("");
  const navigation = useNavigation();

  const handlePost = () => {
    if (!content.trim()) {
      Alert.alert("Empty Post", "Please write something before posting.");
      return;
    }

    // Create a new post object
    const newPost = {
      id: Date.now().toString(),
      author: "Gift Amadi",
      content,
      createdAt: new Date().toISOString(),
      likes: 0,
      comments: [],
      shares: 0,
    };

    // Navigate back to feed with new post
    navigation.navigate("Feed" as never, { newPost } as never);
    setContent(""); // reset
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Post</Text>
      <TextInput
        style={styles.input}
        placeholder="What's on your mind?"
        multiline
        value={content}
        onChangeText={setContent}
      />
      <TouchableOpacity style={styles.button} onPress={handlePost}>
        <Text style={styles.buttonText}>Post</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#D8C9AE",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  input: {
    height: 150,
    borderColor: "#fff",
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    textAlignVertical: "top",
    fontSize: 14,
    marginBottom: 20,
  },
  button: {
    backgroundColor: "black",
    paddingVertical: 14,
    borderRadius: 8,
  },
  buttonText: {
    color: "white",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 16,
  },
});
