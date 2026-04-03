import React, { useState, useEffect } from 'react'
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

  // ✅ Filters
  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  // 🔥 NEW: track new insights
  const [prevInsights, setPrevInsights] = useState([]);
  const [newIds, setNewIds] = useState(new Set());

  useEffect(() => {
    if (!insights.length) return;

    // ✅ FIRST LOAD → don't mark anything as new
    if (prevInsights.length === 0) {
      setPrevInsights(insights);
      return;
    }

    const prevIds = new Set(prevInsights.map(i => i.id));
    const currentIds = insights.map(i => i.id);

    const newOnes = currentIds.filter(id => !prevIds.has(id));

    setNewIds(new Set(newOnes));
    setPrevInsights(insights);

  }, [insights]);

  // ✅ FIXED services extraction
  const services = [
    ...new Set(
      insights.map(i => i?.service).filter(Boolean)
    )
  ];

  // 🔥 Filtering
  const filteredInsights = insights.filter((i) => {

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

  // 🔥 Severity priority sorting
  const priority = {
    CRITICAL: 1,
    HIGH: 2,
    MEDIUM: 3,
    LOW: 4
  };

  const sortedInsights = [...filteredInsights].sort(
    (a, b) => (priority[a.severity] || 5) - (priority[b.severity] || 5)
  );

  return (
    <div className="insights">
      <h1>Cost Insights</h1>

      {error && (
        <div style={{ color: "orange" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

      <FilterBar
        filters={filters}
        setFilters={setFilters}
        services={services}
      />

      {isEmpty && !loading ? (
        <div>No insights available</div>
      ) : (
        <InsightTable
          insights={sortedInsights}
          loading={loading}
          error={error}
          newIds={newIds} 
        />
      )}
    </div>
  )
}

export default Insights