// src/pages/SearchPage.jsx
import React from "react";
import SearchTile from "../components/SearchTile";
import SearchBar from "../components/searchBar";

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

const SearchPage = ({ query, onBack, onSearch }) => {
  return (
    <div className="min-h-screen bg-white text-gray-800 flex flex-col">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white border-b border-gray-200 py-4 px-6 shadow-sm">
        <div className="w-full max-w-6xl mx-auto flex items-center gap-8">
          <div className="text-2xl font-semibold text-blue-600">Perdo</div>
          <div className="flex-1">
            <SearchBar onSearch={onSearch} />
          </div>
          <button
            className="text-xl text-gray-600 hover:underline whitespace-nowrap"
            onClick={onBack}
          >
            ← Back
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="flex-grow w-full max-w-6xl mx-auto px-6 py-6">
        <p className="mb-4 text-sm text-gray-500">
          Showing results for: <span className="text-blue-600">{query}</span>
        </p>
        <div className="space-y-4">
          {dummyResults.map((item, index) => (
            <SearchTile key={index} result={item} />
          ))}
        </div>
      </div>

      {/* Static Pagination Bar */}
      <div className="border-t py-6 px-6 w-full flex justify-start items-center gap-2 text-sm text-blue-600 max-w-6xl mx-auto">
        <button className="px-2 py-1 hover:underline">Previous</button>
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
          <button
            key={num}
            className={`px-2 py-1 rounded ${
              num === 1 ? "font-bold text-black" : "hover:underline"
            }`}
          >
            {num}
          </button>
        ))}
        <button className="px-2 py-1 hover:underline">Next</button>
      </div>
    </div>
  );
};

export default SearchPage;
