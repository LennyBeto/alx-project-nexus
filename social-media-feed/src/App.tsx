import React from "react";
import { ApolloProvider } from "@apollo/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import client from "./graphql/client";
import { Feed } from "./components/feed/Feed";
import "./styles/global.css";

function App() {
  return (
    <ApolloProvider client={client}>
      <Router>
        <div className="min-h-screen bg-dark-50">
          <Routes>
            <Route path="/" element={<Feed />} />
          </Routes>
        </div>
      </Router>
    </ApolloProvider>
  );
}

export default App;
