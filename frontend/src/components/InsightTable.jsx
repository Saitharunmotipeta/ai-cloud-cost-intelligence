import React from 'react'

function InsightTable({ insights }) {
  const getSeverityColor = (severity) => {
    const colors = {
      CRITICAL: '#e74c3c',
      HIGH: '#e67e22',
      MEDIUM: '#f39c12',
      LOW: '#27ae60'
    }
    return colors[severity] || '#95a5a6'
  }

  return (
    <div className="insight-table-container">
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
            <tr key={insight.id || index}>
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
              <td>{new Date(insight.generated_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InsightTable