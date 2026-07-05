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

  // 🔥 BACKEND FILTERING
  const {
    insights = [],
    severity = [],
    daily = [],
    loading,
    error,
    isPartial
  } = useDashboard({
    accountId,
    service: filters.service || null,
    severity: filters.severity === "ALL"
      ? null
      : filters.severity,
  });

  // ✅ services list
  const services = [
    ...new Set(
      (insights || [])
        .map(i => i?.service?.toUpperCase())
        .filter(Boolean)
    )
  ];

  // ✅ Stats
  const totalInsights = useMemo(
    () =>
      severity.reduce(
        (sum, s) => sum + (s?.count || 0),
        0
      ),
    [severity]
  );

  const criticalCount = useMemo(
    () =>
      severity.find(
        s => s?.severity === 'CRITICAL'
      )?.count || 0,
    [severity]
  );

  // ✅ Most affected service
  const serviceMap = {};

  insights.forEach((item) => {
    serviceMap[item.service] =
      (serviceMap[item.service] || 0) + 1;
  });

  const mostAffectedService =
    Object.keys(serviceMap).sort(
      (a, b) => serviceMap[b] - serviceMap[a]
    )[0] || "AWS EC2";

  if (
    error &&
    !insights.length &&
    !severity.length &&
    !daily.length
  ) {
    return (
      <div className="dashboard-error">
        {error.message}
      </div>
    );
  }

  return (

    <div className="dashboard">

      {/* 🔥 HERO SECTION */}

      <div className="ai-hero-card">

        <div className="hero-left">

          <div className="hero-badge">
            AI CLOUD INTELLIGENCE
          </div>

          <h1>
            {criticalCount} abnormal spending patterns detected
          </h1>

          <p>
            AI-powered anomaly detection across your cloud infrastructure.
          </p>

          <div className="hero-stats">

            <div className="hero-stat">
              <span>Total Insights</span>
              <h2>{totalInsights}</h2>
            </div>

            <div className="hero-stat">
              <span>Most Affected Service</span>
              <h2>{mostAffectedService}</h2>
            </div>

          </div>

        </div>

        <div className="hero-right">
          <div className="pulse-circle"></div>
        </div>

      </div>

      {/* 🔥 PARTIAL WARNING */}

      {isPartial && (
        <div className="partial-warning">
          ⚠️ Some dashboard data may be incomplete
        </div>
      )}

      {/* 🔥 FILTER BAR */}

      <FilterBar
        filters={filters}
        setFilters={setFilters}
        services={services}
      />

      {/* 🔥 MODERN METRIC CARDS */}

      <div className="metrics-grid">

        <StatCard
          title="Active Anomalies"
          value={criticalCount}
          color="red"
          loading={loading}
        />

        <StatCard
          title="AI Insights"
          value={totalInsights}
          color="blue"
          loading={loading}
        />

        <StatCard
          title="Services Monitored"
          value={services.length}
          color="green"
          loading={loading}
        />

        <StatCard
          title="Most Affected"
          value={mostAffectedService}
          color="yellow"
          loading={loading}
        />

      </div><br></br>

      {/* 🔥 MAIN GRID */}

      <div className="dashboard-main-grid">

        {/* 🔥 LEFT SIDE */}

        <div className="dashboard-left">

          <div className="glass-card chart-card">

            <h2>Insights Over Time</h2>

            {loading ? (
              <SkeletonChart />
            ) : daily.length === 0 ? (
              <div className="empty-chart">
                No data available
              </div>
            ) : (
              <LineChart data={daily} />
            )}

          </div>

          <div className="glass-card chart-card">

            <h2>Severity Breakdown</h2>

            {loading ? (
              <SkeletonChart />
            ) : severity.length === 0 ? (
              <div className="empty-chart">
                No data available
              </div>
            ) : (
              <PieChart data={severity} />
            )}

          </div>

        </div>

        {/* 🔥 RIGHT SIDE */}

        <div className="dashboard-right">

          <div className="glass-card alert-feed">

            <div className="feed-header">
              <h2>Recent AI Alerts</h2>
            </div>

            {insights.slice(0, 5).map((item) => (

              <div
                className="alert-item"
                key={item.id}
              >

                <div>
                  <span
                    className={`severity-dot ${item.severity?.toLowerCase()}`}
                  ></span>
                </div>

                <div className="alert-content">

                  <h4>{item.service}</h4>

                  <p>
                    {item.explanation?.slice(0, 80)}...
                  </p>

                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

      {/* 🔥 INSIGHTS TABLE */}

      <div className="glass-card insights-section">

        <div className="section-header">
          <h2>Latest AI Insights</h2>
        </div>

        <InsightTable
          insights={(insights || []).slice(0, 10)}
          loading={loading}
          error={error}
        />

      </div>

    </div>
  )
}

export default Dashboard