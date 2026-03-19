import React from 'react'
import { useQuery } from '@apollo/client/react'
import {
  GET_RECENT_INSIGHTS,
  GET_SEVERITY_BREAKDOWN,
  GET_DAILY_INSIGHTS
} from "../api/graphql/queries"

import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'

function Dashboard() {
  const { loading: l1, error: e1, data: insightsData } =
    useQuery(GET_RECENT_INSIGHTS, { variables: { limit: 10 } })

  const { loading: l2, error: e2, data: severityData } =
    useQuery(GET_SEVERITY_BREAKDOWN)

  const { loading: l3, error: e3, data: dailyData } =
    useQuery(GET_DAILY_INSIGHTS)

  if (l1 || l2 || l3) return <div>Loading...</div>
  if (e1 || e2 || e3) return <div>Error loading data</div>

  const insights = insightsData?.recentInsights || []
  const severity = severityData?.severityBreakdown || []
  const daily = dailyData?.dailyInsights || []

  const totalInsights = severity.reduce((sum, s) => sum + s.count, 0)
  const criticalCount = severity.find(s => s.severity === 'CRITICAL')?.count || 0

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <StatCard title="Total Insights" value={totalInsights} />
        <StatCard title="Critical Issues" value={criticalCount} color="red" />
        <StatCard title="Recent Insights" value={insights.length} />
      </div>

      <div className="charts-grid">
        <div>
          <h2>Insights Over Time</h2>
          <LineChart data={daily} />
        </div>

        <div>
          <h2>Severity Breakdown</h2>
          <PieChart data={severity} />
        </div>
      </div>

      <InsightTable insights={insights} />
    </div>
  )
}

export default Dashboard