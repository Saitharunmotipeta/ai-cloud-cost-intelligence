import React, { useState, useEffect } from 'react'
import { useInsights } from "../hooks/useInsights"

import InsightTable from '../components/InsightTable'
import FilterBar from "../components/FilterBar";

function Insights() {

  const accountId = localStorage.getItem("account_id");

  // ✅ Filters (state only, no heavy filtering here)
  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  // 🔥 PASS filters + accountId to hook
  const {
    insights = [],
    loading,
    error,
    isEmpty
  } = useInsights({
    accountId,
    service: filters.service || null,
    severity: filters.severity === "ALL" ? null : filters.severity,
    limit: 50
  });

  // 🔥 Track new insights (unchanged logic)
  const [prevInsights, setPrevInsights] = useState([]);
  const [newIds, setNewIds] = useState(new Set());

  useEffect(() => {
    if (!insights.length) return;

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

  // ✅ Services extraction (safe)
  const services = [
    ...new Set(insights.map(i => i?.service).filter(Boolean))
  ];

  // ❌ REMOVE frontend filtering → backend already filtered

  // 🔥 Sorting only (allowed)
  const priority = {
    CRITICAL: 1,
    HIGH: 2,
    MEDIUM: 3,
    LOW: 4
  };

  const sortedInsights = [...insights].sort(
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