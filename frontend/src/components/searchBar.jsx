// src/components/searchBar.jsx
import React, { useState } from "react";

const SearchBar = ({ onSearch }) => {
  const [searchInput, setSearchInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      onSearch(searchInput.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md flex">
      <input
        type="text"
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)}
        placeholder="Search personal blogs..."
        className="flex-grow px-4 py-2 rounded-l border border-gray-300 focus:outline-none"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-2 rounded-r hover:bg-blue-700"
      >
        Search
      </button>
    </form>
  );
};

export default SearchBar;