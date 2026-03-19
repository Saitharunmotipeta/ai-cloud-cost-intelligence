import React from "react";

function SkeletonTable({ rows = 5 }) {
  return (
    <table className="skeleton-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Severity</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody>
        {Array.from({ length: rows }).map((_, i) => (
          <tr key={i}>
            <td><div className="skeleton-cell shimmer" /></td>
            <td><div className="skeleton-cell shimmer" /></td>
            <td><div className="skeleton-cell shimmer" /></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default SkeletonTable;