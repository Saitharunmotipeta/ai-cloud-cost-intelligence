import React, { useState } from 'react'
import { useInsights } from "../hooks/useInsights"

import InsightTable from '../components/InsightTable'

function Insights() {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL')

  const {
    insights,
    loading,
    error,
    isEmpty
  } = useInsights(50)
  // const loading = true

  const filteredInsights =
    selectedSeverity === 'ALL'
      ? insights
      : insights.filter(i => i?.severity === selectedSeverity)

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      {/* ✅ Partial failure */}
      {error && (
        <div style={{ color: "orange" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

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

      {/* ❌ REMOVE page-level loading */}

      {/* ✅ Let table handle loading */}
      {isEmpty && !loading ? (
        <div>No insights available</div>
      ) : (
        <InsightTable
          insights={filteredInsights}
          loading={loading}
          error={error}
        />
      )}
    </div>
  )
}

export default Insights