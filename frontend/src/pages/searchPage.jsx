// src/pages/SearchPage.jsx
import React from "react";
import SearchTile from "../components/searchTile";

const dummyResults = [
  {
    title: "How I Learned to Love Mondays",
    author: "John Doe",
    summary: "A short story about changing your mindset about Mondays.",
    url: "https://example.com/blog/1",
  },
  {
    title: "The Joy of Minimalism",
    author: "Jane Smith",
    summary: "Exploring the benefits of living with less.",
    url: "https://example.com/blog/2",
  },
  {
    title: "What I Learned from Failing",
    author: "Alex Johnson",
    summary: "Personal growth through failure and recovery.",
    url: "https://example.com/blog/3",
  },
];

const SearchPage = ({ query, onBack }) => {
  return (
    <div className="p-6 bg-white min-h-screen">
      <div className="max-w-3xl mx-auto mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold">
          Search Results for: <span className="text-blue-600">{query}</span>
        </h2>
        <button
          className="text-sm text-gray-600 hover:underline"
          onClick={onBack}
        >
          ← Back
        </button>
      </div>
      <div className="space-y-4 max-w-3xl mx-auto">
        {dummyResults.map((item, index) => (
          <SearchTile key={index} result={item} />
        ))}
      </div>
    </div>
  );
};

export default SearchPage;
