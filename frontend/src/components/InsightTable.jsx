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

  const getImpactColor = (impact) => {
    const colors = {
      high: '#e74c3c',
      medium: '#f39c12',
      low: '#27ae60'
    }
    return colors[impact?.toLowerCase()] || '#95a5a6'
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
            <th>Type</th>
            <th>Impact</th>
            <th>Explanation</th>
            <th>Root Cause</th>
            <th>Action</th>
            <th>Confidence</th>
            <th>Generated</th>
          </tr>
        </thead>

        <tbody>
          {insights.map((insight, index) => (
            <tr key={insight.id || `${insight.service}-${index}`}>

              <td>{insight.service}</td>

              <td>
                <span
                  className="badge"
                  style={{ backgroundColor: getSeverityColor(insight.severity) }}
                >
                  {insight.severity}
                </span>
              </td>

              <td>{insight.anomalyType || 'unknown'}</td>

              <td>
                <span
                  className="badge"
                  style={{ backgroundColor: getImpactColor(insight.impact) }}
                >
                  {insight.impact}
                </span>
              </td>

              <td className="truncate">
                {insight.explanation || insight.message}
              </td>

              <td className="truncate">
                {insight.rootCause || 'N/A'}
              </td>

              <td className="truncate">
                {insight.action || insight.recommendation}
              </td>

              <td>{insight.confidence}</td>

              <td>{formatDate(insight.generated_at)}</td>

            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InsightTable