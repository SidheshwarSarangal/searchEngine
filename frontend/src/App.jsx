// src/App.jsx
import React, { useState } from "react";
import Home from "./pages/home";
import SearchPage from "./pages/searchPage";

const App = () => {
  const [query, setQuery] = useState("");

  return (
    <>
      {query === "" ? (
        <Home onSearch={(q) => setQuery(q)} />
      ) : (
        <SearchPage query={query} onBack={() => setQuery("")} />
      )}
    </>
  );
};

export default App;
