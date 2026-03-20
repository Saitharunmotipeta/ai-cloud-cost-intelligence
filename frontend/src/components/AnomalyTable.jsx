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

  // ✅ Loading
  if (loading) {
    return <SkeletonTable rows={5} />;
  }

  // ✅ Full error
  if (error && anomalies.length === 0) {
    return <div style={{ color: "red" }}>Failed to load anomalies</div>;
  }

  // ✅ Empty
  if (!anomalies.length) {
    return <div>No anomalies detected 🎉</div>;
  }

  return (
    <div className="anomaly-table-container">

      {/* ⚠️ Partial error */}
      {error && (
        <div style={{ color: "orange", marginBottom: "10px" }}>
          ⚠️ Some anomalies may be missing
        </div>
      )}

      <table className="anomaly-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Expected Cost</th>
            <th>Actual Cost</th>
            <th>Deviation</th>
            <th>Severity</th>
            <th>Timestamp</th>
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

                <td style={{ color: "#e74c3c", fontWeight: "bold" }}>
                  +${a.deviation}
                </td>

                <td>
                  <span
                    className="severity-badge"
                    style={{
                      backgroundColor: getSeverityColor(severity),
                    }}
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