import React, { useState } from 'react'
import { useQuery } from '@apollo/client/react'
import { GET_RECENT_INSIGHTS } from "../api/graphql/queries"

import InsightTable from '../components/InsightTable'

function Insights() {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL')

  const { loading, error, data } = useQuery(GET_RECENT_INSIGHTS, {variables: { limit: 50 }})

  if (loading) return <div>Loading insights...</div>
  if (error) return <div>Error loading insights</div>

  const insights = data?.recentInsights || []

  const filteredInsights =
    selectedSeverity === 'ALL'
      ? insights
      : insights.filter(i => i.severity === selectedSeverity)

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      <div className="filters">
        <select
          value={selectedSeverity}
          onChange={(e) => setSelectedSeverity(e.target.value)}
        >
          <option value="ALL">All</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
      </div>

      <InsightTable insights={filteredInsights} />
    </div>
  )
}

export default Insights