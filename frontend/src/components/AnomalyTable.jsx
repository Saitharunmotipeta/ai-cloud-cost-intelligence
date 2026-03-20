import React from "react";
import SkeletonTable from "./skeletons/SkeletonTable";

function AnomalyTable({ anomalies = [], loading = false, error = null }) {

  const getSeverity = (deviation) => {
    if (deviation > 100) return "CRITICAL";
    if (deviation > 50) return "HIGH";
    if (deviation > 20) return "MEDIUM";
    return "LOW";
  };

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
            <th>Expected</th>
            <th>Actual</th>
            <th>Deviation</th>
            <th>Severity</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {anomalies.map((a, index) => {
            const severity = getSeverity(a.deviation);

            return (
              <tr key={`${a.service}-${index}`}>
                <td>{a.service}</td>
                <td>${a.expectedCost}</td>
                <td>${a.actualCost}</td>

                <td className="deviation">
                  +${a.deviation}
                </td>

                <td>
                  <span
                    className="badge"
                    style={{ backgroundColor: getSeverityColor(severity) }}
                  >
                    {severity}
                  </span>
                </td>

                <td>{a.timestamp}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default AnomalyTable;