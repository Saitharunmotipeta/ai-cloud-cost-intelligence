import React from 'react'
import SkeletonTable from './skeletons/SkeletonTable'

function InsightTable({ insights = [], loading = false, error = null }) {

  const getSeverityColor = (severity) => {
    const colors = {
      CRITICAL: '#e74c3c',
      HIGH: '#e67e22',
      MEDIUM: '#f39c12',
      LOW: '#27ae60'
    }
    return colors[severity] || '#95a5a6'
  }

  // ✅ 1. Loading state
  if (loading) {
    return <SkeletonTable rows={5} />
  }

  // ✅ 2. Full error (no data)
  if (error && insights.length === 0) {
    return (
      <div style={{ color: "red" }}>
        Failed to load insights
      </div>
    )
  }

  // ✅ 3. Empty state
  if (!insights.length) {
    return <div>No insights available</div>
  }

  return (
    <div className="insight-table-container">

      {/* ✅ 4. Partial error */}
      {error && (
        <div style={{ color: "orange", marginBottom: "10px" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

      <table className="insight-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Recommendation</th>
            <th>Generated At</th>
          </tr>
        </thead>

        <tbody>
          {insights.map((insight, index) => (
            <tr key={insight.id || `${insight.service}-${index}`}>
              <td>{insight.service}</td>

              <td>
                <span
                  className="severity-badge"
                  style={{ backgroundColor: getSeverityColor(insight.severity) }}
                >
                  {insight.severity}
                </span>
              </td>

              <td>{insight.message}</td>
              <td>{insight.recommendation}</td>
              <td>{insight.generated_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InsightTable