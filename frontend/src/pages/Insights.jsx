import React, { useState } from 'react'
import { useInsights } from "../hooks/useInsights"

import InsightTable from '../components/InsightTable'
import FilterBar from "../components/FilterBar";

function Insights() {

  const {
    insights = [],
    loading,
    error,
    isEmpty
  } = useInsights(50)

  // ✅ Single unified filter state
  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  // ✅ Safe (after insights is available)
  const services = [...new Set(insights.map(i => i.service))];

  // 🔥 Unified filtering logic
  const filteredInsights = insights.filter((i) => {

    const matchSeverity =
      filters.severity === "ALL" || i?.severity === filters.severity;

    const matchService =
      !filters.service || i?.service === filters.service;

    const matchDate =
      !filters.date ||
      i?.generatedAt?.startsWith(filters.date) ||
      i?.generated_at?.startsWith(filters.date);

    return matchSeverity && matchService && matchDate;
  });

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      {/* ⚠️ Partial failure */}
      {error && (
        <div style={{ color: "orange" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

      {/* ✅ FILTER BAR (single source of truth) */}
      <FilterBar
        filters={filters}
        setFilters={setFilters}
        services={services}
      />

      {/* ✅ Table */}
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