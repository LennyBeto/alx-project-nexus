import React from "react";

export const PostSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-lg shadow-card p-6 mb-4 animate-pulse">
      <div className="flex items-start space-x-3">
        <div className="w-12 h-12 bg-dark-200 rounded-full" />
        <div className="flex-1 space-y-3">
          <div className="h-4 bg-dark-200 rounded w-1/4" />
          <div className="h-4 bg-dark-200 rounded w-1/6" />
          <div className="space-y-2 mt-4">
            <div className="h-4 bg-dark-200 rounded" />
            <div className="h-4 bg-dark-200 rounded w-5/6" />
          </div>
          <div className="h-48 bg-dark-200 rounded mt-4" />
          <div className="flex space-x-6 mt-4">
            <div className="h-4 bg-dark-200 rounded w-16" />
            <div className="h-4 bg-dark-200 rounded w-16" />
            <div className="h-4 bg-dark-200 rounded w-16" />
          </div>
        </div>
      </div>
    </div>
  );
};
