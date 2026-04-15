import React from "react";
import SkeletonTable from "./skeletons/SkeletonTable";
import { formatDate } from "../utils/formatDate";

function AnomalyTable({ anomalies = [], loading = false, error = null }) {

  // 🔥 USE BACKEND SEVERITY (NOT CALCULATED)
  const getSeverityColor = (severity) => {
    const colors = {
      CRITICAL: "#e74c3c",
      HIGH: "#e67e22",
      MEDIUM: "#f39c12",
      LOW: "#27ae60",
    };
    return colors[severity] || "#95a5a6";
  };

  if (loading) return <SkeletonTable rows={5} />;

  if (error && anomalies.length === 0) {
    return <div className="error-text">Failed to load anomalies</div>;
  }

  if (!anomalies.length) {
    return <div className="empty-state">No anomalies detected 🎉</div>;
  }

  return (
    <div className="table-wrapper">

      {error && (
        <div className="warning-text">
          ⚠️ Some anomalies may be missing
        </div>
      )}

      <table className="custom-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Severity</th>
            <th>Explanation</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {anomalies.map((a) => (
            <tr key={a.id}>
              <td>{a.service}</td>

              <td>
                <span
                  className="badge"
                  style={{ backgroundColor: getSeverityColor(a.severity) }}
                >
                  {a.severity}
                </span>
              </td>

              <td style={{ maxWidth: "400px" }}>
                {a.explanation}
              </td>

              <td>{formatDate(a.timestamp)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AnomalyTable;