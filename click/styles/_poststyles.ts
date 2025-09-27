import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
    card: {
        backgroundColor: "black",
        padding: 16,
        marginVertical: 4,
        marginHorizontal: 9,
        borderRadius: 12,
        shadowColor: "#575757",
        shadowOpacity: 0.4,
        shadowRadius: 6,
        elevation: 2,
    },
    author: {
        fontWeight: "bold",
        color: "white",
        fontSize: 18,
        marginBottom: 4,
    },
    content: {
        fontSize: 15,
        color: "white",
        marginBottom: 8,
    },
    date: {
        fontSize: 12,
        color: "gray",
        marginBottom: 12,
    },
    actions: {
        flexDirection: "row",
        justifyContent: "space-between",
    },
    button: {
        padding: 6,
    },
    modal: {
        flex: 1,
        padding: 16,
        backgroundColor: "black"
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: "bold",
        color: "white",
        marginBottom: 12,
    },
    commentRow: {
        flexDirection: "row",
        marginBottom: 6,
    },
    commentAuthor: {
        fontWeight: "bold",
        color: "white",
        marginRight: 6,
    },
    commentText: {
        color: "white",
        flex: 1
    },
    inputRow: {
        flexDirection: "row",
        alignItems: "center",
        marginTop: 12,
    },
    input: {
        flex: 1,
        borderWidth: 1,
        borderColor: "gray",
        borderRadius: 6,
        padding: 8,
        marginRight: 8,
        color: "white",
    },
    addButton: {
        color: "skyblue",
        fontWeight: "bold"
    },
    closeBtn: {
        marginTop: 20,
        textAlign: "center",
        color: "red",
        fontWeight: "bold",
    },
    overlay: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "rgba(0,0,0,0.6)",
    },
    repostBox: {
        backgroundColor: "black",
        padding: 16,
        borderRadius: 12,
        width: "80%",
    },
    modalBtn: {
        backgroundColor: "skyblue",
        padding: 10,
        borderRadius: 6,
        marginTop: 8,
    },
    btnText: {
        color: "black",
        fontWeight: "bold",
        textAlign: "center"
    },
});

export { styles };