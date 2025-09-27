import { styles } from "@/styles/_join";
import { Link, useRouter } from "expo-router";
import React, { useState } from "react";
import { Alert, Text, TextInput, TouchableOpacity, View } from "react-native";

export default function Login() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    if (!identifier.trim() || !password.trim()) {
      Alert.alert("Missing fields", "Please enter both email/username and password.");
      return;
    }

    // TODO: replace with real auth call
    // Simulate successful login:
    router.replace("/(home)");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome back</Text>

      <TextInput
        style={styles.input}
        placeholder="Email or username"
        value={identifier}
        onChangeText={setIdentifier}
        autoCapitalize="none"
        keyboardType="email-address"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>

      <View style={styles.row}>
        <Text style={styles.small}>Don't have an account? </Text>
        <Link href="/signup" style={styles.link}>Sign up</Link>
      </View>
    </View>
  );
}

