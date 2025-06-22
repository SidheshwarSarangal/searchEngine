// src/pages/Home.jsx
import React from "react";
import SearchBar from "../components/searchBar";

const Home = ({ onSearch }) => {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100 px-4">
      <h1 className="text-6xl font-bold text-blue-700 mb-8">Perdo</h1>
      <SearchBar onSearch={onSearch} />
    </div>
  );
};

export default Home;
