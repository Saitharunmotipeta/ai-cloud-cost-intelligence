import React from 'react'
import { useQuery } from '@apollo/client/react'
import { GET_RECENT_INSIGHTS, GET_SEVERITY_BREAKDOWN, GET_DAILY_INSIGHTS } from '../graphql/queries'
import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'

function Dashboard() {
  const { loading: insightsLoading, error: insightsError, data: insightsData } = useQuery(GET_RECENT_INSIGHTS, {
    variables: { limit: 10 }
  })

  const { loading: severityLoading, error: severityError, data: severityData } = useQuery(GET_SEVERITY_BREAKDOWN)

  const { loading: dailyLoading, error: dailyError, data: dailyData } = useQuery(GET_DAILY_INSIGHTS)

  if (insightsLoading || severityLoading || dailyLoading) return <div>Loading...</div>
  if (insightsError || severityError || dailyError) return <div>Error loading data</div>

  const totalInsights = severityData?.severity_breakdown?.reduce((sum, item) => sum + item.count, 0) || 0
  const criticalCount = severityData?.severity_breakdown?.find(s => s.severity === 'CRITICAL')?.count || 0

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <StatCard title="Total Insights" value={totalInsights} />
        <StatCard title="Critical Issues" value={criticalCount} color="red" />
        <StatCard title="Services Monitored" value={insightsData?.recent_insights?.length || 0} />
      </div>

      <div className="charts-grid">
        <div className="chart-container">
          <h2>Insights Over Time</h2>
          <LineChart data={dailyData?.daily_insights || []} />
        </div>
        <div className="chart-container">
          <h2>Severity Breakdown</h2>
          <PieChart data={severityData?.severity_breakdown || []} />
        </div>
      </div>

      <div className="recent-insights">
        <h2>Recent Insights</h2>
        <InsightTable insights={insightsData?.recent_insights || []} />
      </div>
    </div>
  )
}

export default Dashboard