import React, { useMemo, useState } from 'react'
import { useDashboard } from "../hooks/useDashboard"

import StatCard from '../components/StatCard'
import InsightTable from '../components/InsightTable'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'
import SkeletonChart from '../components/skeletons/SkeletonChart'
import FilterBar from "../components/FilterBar";

function Dashboard() {

  const {
    insights,
    severity,
    daily,
    loading,
    error,
    isPartial
  } = useDashboard()

  // ✅ Add filters (same pattern as Insights page)
  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  const services = [
    ...new Set(
      insights
        .map(i => i?.service?.toUpperCase())
        .filter(Boolean)
    )
  ];

  // 🔥 Filtered insights (shared logic)
  const filteredInsights = insights.filter((i) => {

    // ✅ apply only if user selected something meaningful
    const matchSeverity =
      !filters.severity || filters.severity === "ALL"
        ? true
        : i?.severity === filters.severity;

    const matchService =
      !filters.service
        ? true
        : i?.service === filters.service;

    const matchDate =
      !filters.date
        ? true
        : i?.generatedAt?.startsWith(filters.date) ||
          i?.generated_at?.startsWith(filters.date);

    return matchSeverity && matchService && matchDate;
  });

  // 🔥 Stats (memoized)
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
        <StatCard title="Filtered Results" value={filteredInsights.length} loading={loading} />
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

      {/* 🔥 TABLE (LIMITED FOR UX) */}
      <InsightTable
        insights={filteredInsights.slice(0, 10)}
        loading={loading}
        error={error}
      />
    </div>
  )
}

export default Dashboard