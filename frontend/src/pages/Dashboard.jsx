import React from 'react'
import { useDashboard } from "../hooks/useDashboard"

import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'

function Dashboard() {
  const {
    insights,
    severity,
    daily,
    loading,
    error,
    isPartial
  } = useDashboard()

  // ✅ Full failure
  if (loading) return <div>Loading...</div>

  if (error && !insights.length && !severity.length && !daily.length) {
    return <div>{error.message}</div>
  }

  // ✅ Safe calculations
  const totalInsights = severity.reduce((sum, s) => sum + (s?.count || 0), 0)

  const criticalCount =
    severity.find(s => s?.severity === 'CRITICAL')?.count || 0

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      {/* ✅ Partial failure banner */}
      {isPartial && (
        <div style={{ color: "orange" }}>
          ⚠️ Some dashboard data may be incomplete
        </div>
      )}

      <div className="stats-grid">
        <StatCard title="Total Insights" value={totalInsights} />
        <StatCard title="Critical Issues" value={criticalCount} color="red" />
        <StatCard title="Recent Insights" value={insights.length} />
      </div>

      <div className="charts-grid">
        <div>
          <h2>Insights Over Time</h2>
          <LineChart data={daily || []} />
        </div>

        <div>
          <h2>Severity Breakdown</h2>
          <PieChart data={severity || []} />
        </div>
      </div>

      <InsightTable insights={insights || []} />
    </div>
  )
}

export default Dashboard