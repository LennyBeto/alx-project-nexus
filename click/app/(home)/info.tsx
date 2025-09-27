import React, { useState } from "react";
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from "react-native";
import { FontAwesome6 } from "@expo/vector-icons";

export default function Notifications() {
  // Mock notification data
  const [notifications, setNotifications] = useState([
    {
      id: "1",
      type: "like",
      message: "Jane liked your post",
      time: "2m ago",
      read: false,
    },
    {
      id: "2",
      type: "comment",
      message: "Alex commented: 'Nice work!'",
      time: "10m ago",
      read: false,
    },
    {
      id: "3",
      type: "share",
      message: "Chris shared your post",
      time: "1h ago",
      read: true,
    },
  ]);

  const renderIcon = (type: string) => {
    switch (type) {
      case "like":
        return <FontAwesome6 name="heart" size={18} color="red" />;
      case "comment":
        return <FontAwesome6 name="comment" size={18} color="blue" />;
      case "share":
        return <FontAwesome6 name="share" size={18} color="green" />;
      default:
        return <FontAwesome6 name="bell" size={18} color="gray" />;
    }
  };

  const handleMarkAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((n) =>
        n.id === id ? { ...n, read: true } : n
      )
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={notifications}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.card, !item.read && styles.unread]}
            onPress={() => handleMarkAsRead(item.id)}
          >
            <View style={styles.icon}>{renderIcon(item.type)}</View>
            <View style={styles.textBox}>
              <Text style={styles.message}>{item.message}</Text>
              <Text style={styles.time}>{item.time}</Text>
            </View>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <Text style={styles.emptyText}>No notifications yet</Text>
        }
      />
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
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 15,
  },
  card: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
    backgroundColor: "#f9f9f9",
  },
  unread: {
    backgroundColor: "#e8f0fe",
  },
  icon: {
    marginRight: 12,
  },
  textBox: {
    flex: 1,
  },
  message: {
    fontSize: 14,
    fontWeight: "500",
  },
  time: {
    fontSize: 12,
    color: "gray",
  },
  emptyText: {
    textAlign: "center",
    marginTop: 50,
    color: "gray",
  },
});
