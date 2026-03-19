import React from "react";

function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton-title shimmer" />
      <div className="skeleton-value shimmer" />
    </div>
  );
}

export default SkeletonCard;