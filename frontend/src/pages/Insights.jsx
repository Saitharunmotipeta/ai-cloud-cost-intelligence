import React, {
  useState,
  useEffect,
  useMemo
} from "react";

import {
  Search
} from "lucide-react";

import { useInsights } from "../hooks/useInsights";

import InsightTable from "../components/InsightTable";

import FilterBar from "../components/FilterBar";

function Insights() {

  const accountId =
    localStorage.getItem("account_id");

  /* =========================
     FILTERS
  ========================= */

  const [filters, setFilters] = useState({
    severity: "ALL",
    service: "",
    date: ""
  });

  /* =========================
     SEARCH
  ========================= */

  const [searchQuery, setSearchQuery] =
    useState("");

  const [debouncedSearch, setDebouncedSearch] =
    useState("");

  /* =========================
     PAGINATION
  ========================= */

  const [currentPage, setCurrentPage] =
    useState(1);

  const ITEMS_PER_PAGE = 7;

  /* =========================
     INSIGHTS
  ========================= */

  const {
    insights = [],
    loading,
    error,
    isEmpty
  } = useInsights({
    accountId,
    service: filters.service || null,
    severity:
      filters.severity === "ALL"
        ? null
        : filters.severity,
    limit: 50
  });

  /* =========================
     DEBOUNCE
  ========================= */

  useEffect(() => {

    const timer = setTimeout(() => {

      setDebouncedSearch(
        searchQuery
      );

    }, 400);

    return () => clearTimeout(timer);

  }, [searchQuery]);

  /* =========================
     NEW INSIGHTS TRACKING
  ========================= */

  const [prevInsights, setPrevInsights] =
    useState([]);

  const [newIds, setNewIds] =
    useState(new Set());

  useEffect(() => {

    if (!insights.length) return;

    if (prevInsights.length === 0) {

      setPrevInsights(insights);

      return;

    }

    const prevIds = new Set(
      prevInsights.map(i => i.id)
    );

    const currentIds =
      insights.map(i => i.id);

    const newOnes =
      currentIds.filter(
        id => !prevIds.has(id)
      );

    setNewIds(new Set(newOnes));

    setPrevInsights(insights);

  }, [insights]);

  /* =========================
     SERVICES
  ========================= */

  const services = [

    ...new Set(
      insights
        .map(i => i?.service)
        .filter(Boolean)
    )

  ];

  /* =========================
     SORTING
  ========================= */

  const priority = {
    CRITICAL: 1,
    HIGH: 2,
    MEDIUM: 3,
    LOW: 4
  };

  const sortedInsights =
    [...insights].sort(
      (a, b) =>
        (priority[a.severity] || 5)
        -
        (priority[b.severity] || 5)
    );

  /* =========================
     SEARCH FILTERING
  ========================= */

  const filteredInsights =
    useMemo(() => {

      if (!debouncedSearch.trim()) {
        return sortedInsights;
      }

      const query =
        debouncedSearch.toLowerCase();

      return sortedInsights.filter(
        (insight) => {

          return (

            insight.service
              ?.toLowerCase()
              .includes(query)

            ||

            insight.explanation
              ?.toLowerCase()
              .includes(query)

            ||

            insight.message
              ?.toLowerCase()
              .includes(query)

            ||

            insight.recommendation
              ?.toLowerCase()
              .includes(query)

            ||

            insight.action
              ?.toLowerCase()
              .includes(query)

            ||

            insight.rootCause
              ?.toLowerCase()
              .includes(query)

            ||

            insight.anomalyType
              ?.toLowerCase()
              .includes(query)

          );

        }
      );

    }, [
      debouncedSearch,
      sortedInsights
    ]);

  /* =========================
     RESET PAGE
  ========================= */

  useEffect(() => {

    setCurrentPage(1);

  }, [
    debouncedSearch,
    filters
  ]);

  /* =========================
     PAGINATION
  ========================= */

  const startIndex =
    (currentPage - 1)
    * ITEMS_PER_PAGE;

  const paginatedInsights =
    filteredInsights.slice(
      startIndex,
      startIndex + ITEMS_PER_PAGE
    );

  const totalPages = Math.ceil(
    filteredInsights.length
    / ITEMS_PER_PAGE
  );

  return (

    <div className="insights-page">

      {/* =========================
          TOP BAR
      ========================= */}

      <div className="insights-topbar">

        {/* LEFT */}

        <div className="insights-heading">

          <h1>
            Latest AI Insights
          </h1>

        </div>

        {/* RIGHT */}

        <div className="insights-controls">

          {/* FILTER */}

          <div className="severity-filter">

            <select
              value={filters.severity}
              onChange={(e) => {

                setFilters({
                  ...filters,
                  severity: e.target.value
                });

                setCurrentPage(1);

              }}
            >

              <option value="ALL">
                All Severity
              </option>

              <option value="CRITICAL">
                Critical
              </option>

              <option value="HIGH">
                High
              </option>

              <option value="MEDIUM">
                Medium
              </option>

              <option value="LOW">
                Low
              </option>

            </select>

          </div>

          {/* SEARCH */}

          <div className="insights-search">

            <Search
              size={18}
              className="insights-search-icon"
            />

            <input
              type="text"
              placeholder="Search insights, services..."
              value={searchQuery}
              onChange={(e) =>
                setSearchQuery(
                  e.target.value
                )
              }
            />

          </div>

        </div>

      </div>

      {/* =========================
          ERROR
      ========================= */}

      {error && (

        <div className="insight-warning">

          ⚠️ Some insights may be missing

        </div>

      )}

      {/* =========================
          TABLE
      ========================= */}

      {isEmpty && !loading ? (

        <div className="empty-state">
          No insights available
        </div>

      ) : (

        <>

          <InsightTable
            insights={paginatedInsights}
            loading={loading}
            error={error}
            newIds={newIds}
            itemsPerPage={7}
            variant="insights"
          />

          {/* =========================
              PAGINATION
          ========================= */}

          {totalPages > 1 && (

            <div className="pagination">

              <button
                disabled={currentPage === 1}
                onClick={() =>
                  setCurrentPage(prev => prev - 1)
                }
              >
                Prev
              </button>

              {[...Array(totalPages)].map((_, index) => (

                <button
                  key={index}
                  className={
                    currentPage === index + 1
                      ? "active-page"
                      : ""
                  }
                  onClick={() =>
                    setCurrentPage(index + 1)
                  }
                >
                  {index + 1}
                </button>

              ))}

              <button
                disabled={
                  currentPage === totalPages
                }
                onClick={() =>
                  setCurrentPage(prev => prev + 1)
                }
              >
                Next
              </button>

            </div>

          )}

        </>

      )}

    </div>

  );

}

export default Insights;