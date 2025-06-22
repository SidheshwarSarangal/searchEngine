// src/components/SearchTile.jsx
import React from "react";

const SearchTile = ({ result }) => {
  return (
    <div className="border border-gray-300 p-4 rounded shadow hover:shadow-md transition">
      <a href={result.url} target="_blank" rel="noopener noreferrer">
        <h3 className="text-xl font-semibold text-blue-700 hover:underline">
          {result.title}
        </h3>
      </a>
      <p className="text-gray-600">By {result.author || "Unknown"}</p>
      <p className="mt-2 text-gray-800">{result.summary}</p>
    </div>
  );
};

export default SearchTile;
