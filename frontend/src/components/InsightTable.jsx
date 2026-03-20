import React from 'react'
import SkeletonTable from './skeletons/SkeletonTable'
import { formatDate } from '../utils/formatDate'

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

  if (loading) return <SkeletonTable rows={5} />

  if (error && insights.length === 0) {
    return <div className="error-text">Failed to load insights</div>
  }

  if (!insights.length) {
    return <div className="empty-state">No insights available</div>
  }

  return (
    <div className="table-wrapper">

      {error && (
        <div className="warning-text">
          ⚠️ Some insights may be missing
        </div>
      )}

      <table className="custom-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Recommendation</th>
            <th>Generated</th>
          </tr>
        </thead>

        <tbody>
          {insights.map((insight, index) => (
            <tr key={insight.insight_id || `${insight.service}-${index}`}>
              <td>{insight.service}</td>

              <td>
                <span
                  className="badge"
                  style={{ backgroundColor: getSeverityColor(insight.severity) }}
                >
                  {insight.severity}
                </span>
              </td>

              <td className="truncate">{insight.message}</td>
              <td className="truncate">{insight.recommendation}</td>

              {/* 🔥 FIXED + FORMATTED */}
              <td>{formatDate(insight.generated_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InsightTable