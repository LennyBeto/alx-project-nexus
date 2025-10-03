// src/apollo/client.js
import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  from,
} from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Platform } from "react-native";

// Your backend GraphQL endpoint
// Adjust this logic as needed for your environment (e.g., Android emulator, iOS simulator, production)
const API_URL = __DEV__
  ? Platform.OS === "android"
    ? "http://10.0.2.2:8000/graphql/" // Android emulator
    : "http://localhost:8000/graphql/" // iOS simulator or other dev
  : "https://your-backend.vercel.app/graphql/"; // Production

const httpLink = createHttpLink({
  uri: API_URL,
});

// Authentication link to include JWT token in headers
const authLink = setContext(async (_, { headers }) => {
  try {
    const token = await AsyncStorage.getItem("authToken");
    return {
      headers: {
        ...headers,
        authorization: token ? `Bearer ${token}` : "",
      },
    };
  } catch (error) {
    console.error("Error getting auth token:", error);
    return { headers };
  }
});

// Error link for handling GraphQL errors
const errorLink = onError(
  ({ graphQLErrors, networkError, operation, forward }) => {
    if (graphQLErrors) {
      graphQLErrors.forEach(({ message, locations, path }) => {
        console.error(
          `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
        );
      });
    }

    if (networkError) {
      console.error(`[Network error]: ${networkError}`);

      // Handle authentication errors
      if (networkError.statusCode === 401) {
        // Clear stored token and redirect to login
        AsyncStorage.removeItem("authToken");
        // You might want to navigate to login screen here
      }
    }
  }
);

// Create Apollo Client
const client = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      Post: {
        fields: {
          comments: {
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            },
          },
        },
      },
      Query: {
        fields: {
          posts: {
            keyArgs: false,
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            },
          },
          feed: {
            keyArgs: false,
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      errorPolicy: "all",
    },
    query: {
      errorPolicy: "all",
    },
  },
});

export default client;
