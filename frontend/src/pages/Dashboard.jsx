import React from 'react'
import { useDashboard } from "../hooks/useDashboard"

import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'
import SkeletonChart from '../components/skeletons/SkeletonChart'

function Dashboard() {
  const {
    insights,
    severity,
    daily,
    loading,
    error,
    isPartial
  } = useDashboard()

  if (error && !insights.length && !severity.length && !daily.length) {
    return <div>{error.message}</div>
  }

  const totalInsights = severity.reduce((sum, s) => sum + (s?.count || 0), 0)

  const criticalCount =
    severity.find(s => s?.severity === 'CRITICAL')?.count || 0

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      {/* ✅ Partial failure */}
      {isPartial && (
        <div style={{ color: "orange" }}>
          ⚠️ Some dashboard data may be incomplete
        </div>
      )}

      {/* ✅ Cards now handle loading */}
      <div className="stats-grid">
        <StatCard title="Total Insights" value={totalInsights} loading={loading} />
        <StatCard title="Critical Issues" value={criticalCount} color="red" loading={loading} />
        <StatCard title="Recent Insights" value={insights.length} loading={loading} />
      </div>

      <div className="charts-grid">
        <div>
          <h2>Insights Over Time</h2>
          {loading ? <SkeletonChart /> : <LineChart data={daily || []} />}
        </div>

        <div>
          <h2>Severity Breakdown</h2>
          {loading ? <SkeletonChart /> : <PieChart data={severity || []} />}
        </div>
      </div>

      {/* Step 3 will upgrade this */}
      <InsightTable insights={insights || []} loading={loading} error={error} />
    </div>
  )
}

export default Dashboard