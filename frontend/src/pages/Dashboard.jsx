import React, { useMemo, useState } from 'react'
import { useDashboard } from "../hooks/useDashboard"

import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'
import SkeletonChart from '../components/skeletons/SkeletonChart'
import FilterBar from "../components/FilterBar";

function Dashboard() {

  const accountId = localStorage.getItem("account_id");

  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  // 🔥 BACKEND FILTERING (IMPORTANT)
  const {
    insights,
    severity,
    daily,
    loading,
    error,
    isPartial
  } = useDashboard({
    accountId,
    service: filters.service || null,
    severity: filters.severity === "ALL" ? null : filters.severity,
  });

  // ✅ services list (safe)
  const services = [
    ...new Set(
      insights
        .map(i => i?.service?.toUpperCase())
        .filter(Boolean)
    )
  ];

  // 🔥 Stats (correct now)
  const totalInsights = useMemo(
    () => severity.reduce((sum, s) => sum + (s?.count || 0), 0),
    [severity]
  );

  const criticalCount = useMemo(
    () => severity.find(s => s?.severity === 'CRITICAL')?.count || 0,
    [severity]
  );

  if (error && !insights.length && !severity.length && !daily.length) {
    return <div>{error.message}</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      {isPartial && (
        <div style={{ color: "orange" }}>
          ⚠️ Some dashboard data may be incomplete
        </div>
      )}

      {/* 🔥 FILTER BAR */}
      <FilterBar
        filters={filters}
        setFilters={setFilters}
        services={services}
      />

      {/* 🔥 STAT CARDS */}
      <div className="stats-grid">
        <StatCard title="Total Insights" value={totalInsights} loading={loading} />
        <StatCard title="Critical Issues" value={criticalCount} color="red" loading={loading} />
        <StatCard title="Filtered Results" value={insights.length} loading={loading} />
      </div>

      {/* 🔥 CHARTS */}
      <div className="charts-grid">

        <div>
          <h2>Insights Over Time</h2>
          {loading ? (
            <SkeletonChart />
          ) : daily.length === 0 ? (
            <div className="empty-chart">No data available</div>
          ) : (
            <LineChart data={daily} />
          )}
        </div>

        <div>
          <h2>Severity Breakdown</h2>
          {loading ? (
            <SkeletonChart />
          ) : severity.length === 0 ? (
            <div className="empty-chart">No data available</div>
          ) : (
            <PieChart data={severity} />
          )}
        </div>

      </div>

      {/* 🔥 TABLE */}
      <InsightTable
        insights={insights.slice(0, 10)}
        loading={loading}
        error={error}
      />
    </div>
  )
}

export default Dashboard