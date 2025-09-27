import { styles } from "@/styles/_join";
import { Link, useRouter } from "expo-router";
import React, { useState } from "react";
import { Alert, Text, TextInput, TouchableOpacity, View } from "react-native";

export default function Signup() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const handleSignup = () => {
    if (!username.trim() || !email.trim() || !password.trim() || !confirm.trim()) {
      Alert.alert("Missing fields", "Please fill out all fields.");
      return;
    }
    if (password !== confirm) {
      Alert.alert("Passwords don't match", "Please confirm your password.");
      return;
    }

    // TODO: replace with real registration call
    // Simulate successful registration:
    router.replace("/(home)");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create account</Text>

      <TextInput style={styles.input} placeholder="Username" value={username} onChangeText={setUsername} />
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput style={styles.input} placeholder="Password" secureTextEntry value={password} onChangeText={setPassword} />
      <TextInput
        style={styles.input}
        placeholder="Confirm password"
        secureTextEntry
        value={confirm}
        onChangeText={setConfirm}
      />

      <TouchableOpacity style={styles.button} onPress={handleSignup}>
        <Text style={styles.buttonText}>Sign Up</Text>
      </TouchableOpacity>

      <View style={styles.row}>
        <Text style={styles.small}>Already have an account? </Text>
        <Link href="/login" style={styles.link}>Log in</Link>
      </View>
    </View>
  );
}

