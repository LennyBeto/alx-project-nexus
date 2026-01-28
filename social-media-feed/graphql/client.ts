import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";

const client = new ApolloClient({
  link: new HttpLink({
    uri: "YOUR_GRAPHQL_ENDPOINT", // Replace with your GraphQL endpoint
  }),
  cache: new InMemoryCache(),
});

export default client;
