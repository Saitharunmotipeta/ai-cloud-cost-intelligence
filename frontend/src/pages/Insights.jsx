import React, { useState } from 'react'
import { useQuery } from '@apollo/client/react'
import { GET_RECENT_INSIGHTS } from '../graphql/queries'
import InsightTable from '../components/InsightTable'

function Insights() {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL')
  const { loading, error, data } = useQuery(GET_RECENT_INSIGHTS, {
    variables: { limit: 50 }
  })

  if (loading) return <div>Loading insights...</div>
  if (error) return <div>Error loading insights: {error.message}</div>

  const insights = data?.recent_insights || []
  const filteredInsights = selectedSeverity === 'ALL'
    ? insights
    : insights.filter(insight => insight.severity === selectedSeverity)

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      <div className="filters">
        <label htmlFor="severity-filter">Filter by Severity:</label>
        <select
          id="severity-filter"
          value={selectedSeverity}
          onChange={(e) => setSelectedSeverity(e.target.value)}
        >
          <option value="ALL">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
      </div>

      <div className="insights-summary">
        <p>Showing {filteredInsights.length} of {insights.length} insights</p>
      </div>

      <InsightTable insights={filteredInsights} />
    </div>
  )
}

export default Insights