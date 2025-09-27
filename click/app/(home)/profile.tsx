import { router } from "expo-router";
import React from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from "react-native";

export default function Profile() {
  // Mock user data (replace with real auth/user data later)
  const user = {
    name: "Gift Amadi",
    username: "@gift_dev",
    bio: "Frontend developer in training 🚀 | Learning React Native & web.",
    stats: {
      posts: 12,
      followers: 120,
      following: 88,
    },
  };

  const handleLogout = () => {
    // replace with real logout logic later
    console.log("User logged out");
    router.replace ("/");
    };

  return (
    <ScrollView style={styles.container}>
      {/* Avatar + Name */}
      <View style={styles.header}>
        <Image source={require("@/assets/images/user-image.png")} style={styles.avatar} />
        <Text style={styles.name}>{user.name}</Text>
        <Text style={styles.username}>{user.username}</Text>
        <Text style={styles.bio}>{user.bio}</Text>
      </View>

      {/* Stats */}
      <View style={styles.statsContainer}>
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>{user.stats.posts}</Text>
          <Text style={styles.statLabel}>Posts</Text>
        </View>
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>{user.stats.followers}</Text>
          <Text style={styles.statLabel}>Followers</Text>
        </View>
        <View style={styles.statBox}>
          <Text style={styles.statNumber}>{user.stats.following}</Text>
          <Text style={styles.statLabel}>Following</Text>
        </View>
      </View>

      {/* Buttons */}
      <View style={styles.buttonsContainer}>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Edit Profile</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.button, styles.outlineButton]}>
          <Text style={styles.outlineText}>Settings</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.button, styles.logoutButton]} onPress={handleLogout}>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#D8C9AE",
    padding: 20,
  },
  header: {
    alignItems: "center",
    marginBottom: 20,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 60,
    marginBottom: 10,
  },
  name: {
    fontSize: 22,
    fontWeight: "bold",
  },
  username: {
    fontSize: 14,
    color: "gray",
    marginBottom: 8,
  },
  bio: {
    fontSize: 14,
    textAlign: "center",
    paddingHorizontal: 20,
    color: "#444",
  },
  statsContainer: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginVertical: 20,
  },
  statBox: {
    alignItems: "center",
  },
  statNumber: {
    fontSize: 18,
    fontWeight: "bold",
  },
  statLabel: {
    fontSize: 12,
    color: "gray",
  },
  buttonsContainer: {
    marginTop: 10,
  },
  button: {
    backgroundColor: "black",
    paddingVertical: 12,
    borderRadius: 6,
    marginBottom: 12,
  },
  buttonText: {
    color: "white",
    fontSize: 14,
    textAlign: "center",
    fontWeight: "bold",
  },
  outlineButton: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "black",
  },
  outlineText: {
    color: "black",
    fontWeight: "bold",
    textAlign: "center",
  },
  logoutButton: {
    backgroundColor: "#f8d7da",
  },
  logoutText: {
    color: "#b00020",
    fontWeight: "bold",
    textAlign: "center",
  },
});
