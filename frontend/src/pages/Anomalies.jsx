import React, { useState, useMemo } from "react";

import {
  ShieldAlert,
  Activity,
  AlertTriangle,
  Radar
} from "lucide-react";

import { useAnomalies } from "../hooks/useAnomalies";

import AnomalyTable from "../components/AnomalyTable";

function Anomalies() {

  const accountId =
    localStorage.getItem("account_id");

  const {
    anomalies,
    loading,
    error
  } = useAnomalies({
    accountId
  });

  const [selectedSeverity, setSelectedSeverity] =
    useState("ALL");

  const [selectedDate, setSelectedDate] =
    useState("");

  const [currentPage, setCurrentPage] =
    useState(1);

  const ITEMS_PER_PAGE = 7;

  /* =========================
     FILTERING
  ========================= */

  const filteredAnomalies =
    anomalies.filter((a) => {

      const matchSeverity =
        selectedSeverity === "ALL" ||
        a.severity === selectedSeverity;

      const matchDate =
        !selectedDate ||
        a.timestamp?.startsWith(selectedDate);

      return (
        matchSeverity &&
        matchDate
      );

    });

  /* =========================
     PAGINATION
  ========================= */

  const startIndex =
    (currentPage - 1) * ITEMS_PER_PAGE;

  const paginatedAnomalies =
    filteredAnomalies.slice(
      startIndex,
      startIndex + ITEMS_PER_PAGE
    );

  const totalPages = Math.ceil(
    filteredAnomalies.length /
    ITEMS_PER_PAGE
  );

  /* =========================
     STATS
  ========================= */

  const criticalCount = useMemo(
    () =>
      anomalies.filter(
        a => a.severity === "CRITICAL"
      ).length,
    [anomalies]
  );

  const highCount = useMemo(
    () =>
      anomalies.filter(
        a => a.severity === "HIGH"
      ).length,
    [anomalies]
  );

  return (

    <div className="anomalies-page">

      {/* =========================
          HERO
      ========================= */}

      <div className="anomaly-hero">

        <div className="anomaly-hero-left">

          <div className="hero-badge">
            AI INCIDENT MONITORING
          </div>

          <h1>
            Real-time anomaly detection
            across cloud infrastructure
          </h1>

          <p>
            Monitor abnormal spending,
            detect suspicious activity,
            and investigate critical
            cloud events instantly.
          </p>

        </div>

        <div className="anomaly-hero-right">

          <div className="hero-pulse">

            <Radar size={42} />

          </div>

        </div>

      </div>

      {/* =========================
          STATS
      ========================= */}

      <div className="anomaly-stats-grid">

        <div className="anomaly-stat-card critical">

          <div className="anomaly-stat-icon">
            <ShieldAlert size={22} />
          </div>

          <h2>
            {criticalCount}
          </h2>

          <span>
            Critical Alerts
          </span>

        </div>

        <div className="anomaly-stat-card high">

          <div className="anomaly-stat-icon">
            <AlertTriangle size={22} />
          </div>

          <h2>
            {highCount}
          </h2>

          <span>
            High Severity Events
          </span>

        </div>

        <div className="anomaly-stat-card active">

          <div className="anomaly-stat-icon">
            <Activity size={22} />
          </div>

          <h2>
            {anomalies.length}
          </h2>

          <span>
            Active Monitored Events
          </span>

        </div>

      </div>

      {/* =========================
          FILTERS
      ========================= */}

      <div className="modern-filter-bar">

        <div className="filter-group">

          <select
            className="modern-select"
            value={selectedSeverity}
            onChange={(e) => {
              setSelectedSeverity(
                e.target.value
              );

              setCurrentPage(1);
            }}
          >

            <option value="ALL">
              All Severities
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

        <input
          className="modern-date-input"
          type="date"
          value={selectedDate}
          onChange={(e) => {
            setSelectedDate(
              e.target.value
            );

            setCurrentPage(1);
          }}
        />

      </div>

      {/* =========================
          TABLE
      ========================= */}

      <AnomalyTable
        anomalies={paginatedAnomalies}
        loading={loading}
        error={error}
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

    </div>

  );
}

export default Anomalies;