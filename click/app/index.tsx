import React from "react";
import { View, Text, TouchableOpacity} from "react-native";
import { useRouter } from "expo-router";
import { styles } from "../styles/_mainstyles";

export default function Landing() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Click</Text>
      <Text style={styles.subtitle}>Simplicity in Authentic Connections</Text>

      <TouchableOpacity style={styles.primaryButton} onPress={() => router.push("/login")}>
        <Text style={styles.primaryButtonText}>Login</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.secondaryButton} onPress={() => router.push("/signup")}>
        <Text style={styles.secondaryButtonText}>Sign Up</Text>
      </TouchableOpacity>
    </View>
  );
}

