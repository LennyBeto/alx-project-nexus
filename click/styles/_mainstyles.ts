import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    backgroundColor: "#D8C9AE",
  },
  title: { 
    fontSize: 50, 
    fontWeight: "800", 
    marginBottom: 6 
  },
  subtitle: { 
    fontSize: 16, 
    color: "#666", 
    marginBottom: 47, 
    textAlign: "center" 
  },
  primaryButton: {
    width: "30%",
    paddingVertical: 14,
    alignItems: "center",
    backgroundColor: "#575757",
    borderRadius: 50,
    marginBottom: 12,
  },
  primaryButtonText: { 
    color: "#fff", 
    fontWeight: "600" 
  },
  secondaryButton: {
    width: "30%",
    paddingVertical: 14,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#000",
    borderRadius: 50,
  },
  secondaryButtonText: { 
    color: "#000", 
    fontWeight: "600" 
  },
});

export {styles};