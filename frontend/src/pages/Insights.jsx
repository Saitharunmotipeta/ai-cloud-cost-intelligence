import React, { useState, useEffect } from 'react'
import { useInsights } from "../hooks/useInsights"

import InsightTable from '../components/InsightTable'
import FilterBar from "../components/FilterBar";

function Insights() {

  const accountId = localStorage.getItem("account_id");

  // ✅ Filters
  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  // 🔥 PAGINATION
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 7;

  // 🔥 INSIGHTS
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

  // 🔥 Track new insights
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

    const newOnes = currentIds.filter(
      id => !prevIds.has(id)
    );

    setNewIds(new Set(newOnes));

    setPrevInsights(insights);

  }, [insights]);

  // ✅ Services extraction
  const services = [
    ...new Set(
      insights
        .map(i => i?.service)
        .filter(Boolean)
    )
  ];

  // 🔥 SORTING
  const priority = {
    CRITICAL: 1,
    HIGH: 2,
    MEDIUM: 3,
    LOW: 4
  };

  const sortedInsights = [...insights].sort(
    (a, b) =>
      (priority[a.severity] || 5)
      - (priority[b.severity] || 5)
  );

  // 🔥 PAGINATION LOGIC
  const startIndex =
    (currentPage - 1) * ITEMS_PER_PAGE;

  const paginatedInsights =
    sortedInsights.slice(
      startIndex,
      startIndex + ITEMS_PER_PAGE
    );

  const totalPages = Math.ceil(
    sortedInsights.length / ITEMS_PER_PAGE
  );

  return (
    <div className="insights">

      {/* <h1>Cost Insights</h1> */}

      {error && (
        <div style={{ color: "orange" }}>
          ⚠️ Some insights may be missing
        </div>
      )}

      <FilterBar
        filters={filters}
        setFilters={(newFilters) => {
          setFilters(newFilters);
          setCurrentPage(1);
        }}
        services={services}
      />

      {isEmpty && !loading ? (

        <div>No insights available</div>

      ) : (

        <>
          <InsightTable
            insights={sortedInsights}
            loading={loading}
            error={error}
            newIds={newIds}
            itemsPerPage={7}
            variant="insights"
          />



        </>
      )}

    </div>
  )
}

export default Insights