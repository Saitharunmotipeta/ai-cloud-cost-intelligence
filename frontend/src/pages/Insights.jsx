import React, { useState } from 'react'
import { useInsights } from "../hooks/useInsights"

import InsightTable from '../components/InsightTable'

function Insights() {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL')
  const [selectedDate, setSelectedDate] = useState("")

  const {
    insights,
    loading,
    error,
    isEmpty
  } = useInsights(50)

  // 🔥 Filtering logic (severity + date)
  const filteredInsights = insights.filter((i) => {
    const matchSeverity =
      selectedSeverity === 'ALL' || i?.severity === selectedSeverity

    const matchDate =
      !selectedDate ||
      i?.generated_at?.startsWith(selectedDate)

    return matchSeverity && matchDate
  })

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      {/* ✅ Partial failure */}
      {error && (
        <div style={{ color: "orange" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

      {/* 🔥 FILTERS */}
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

        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
        />
      </div>

      {/* ✅ Table handles loading */}
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