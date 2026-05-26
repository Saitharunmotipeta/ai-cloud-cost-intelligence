import React, { useState } from "react";
import { useAnomalies } from "../hooks/useAnomalies";
import AnomalyTable from "../components/AnomalyTable";

function Anomalies() {

  const accountId = localStorage.getItem("account_id");

  const { anomalies, loading, error } = useAnomalies({
    accountId
  });

  const [selectedSeverity, setSelectedSeverity] = useState("ALL");
  const [selectedDate, setSelectedDate] = useState("");

  // 🔥 PAGINATION
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 7;

  // 🔥 FILTERING
  const filteredAnomalies = anomalies.filter((a) => {

    const matchSeverity =
      selectedSeverity === "ALL" || a.severity === selectedSeverity;

    const matchDate =
      !selectedDate || a.timestamp?.startsWith(selectedDate);

    return matchSeverity && matchDate;
  });

  // 🔥 PAGINATION LOGIC
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;

  const paginatedAnomalies = filteredAnomalies.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );

  const totalPages = Math.ceil(
    filteredAnomalies.length / ITEMS_PER_PAGE
  );

  return (
    <div className="anomalies">

      {/* <h1>Cost Anomalies</h1> */}

      {/* 🔥 FILTERS */}
      <div className="filters">

        <select
          value={selectedSeverity}
          onChange={(e) => {
            setSelectedSeverity(e.target.value);
            setCurrentPage(1);
          }}
        >
          <option value="ALL">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>

        <input
          type="date"
          value={selectedDate}
          onChange={(e) => {
            setSelectedDate(e.target.value);
            setCurrentPage(1);
          }}
        />

      </div>

      <AnomalyTable
        anomalies={paginatedAnomalies}
        loading={loading}
        error={error}
      />

      {/* 🔥 PAGINATION */}
      {totalPages > 1 && (
        <div className="pagination">

          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Prev
          </button>

          {Array.from({ length: totalPages }, (_, index) => (
            <button
              key={index + 1}
              className={
                currentPage === index + 1
                  ? "active-page"
                  : ""
              }
              onClick={() => setCurrentPage(index + 1)}
            >
              {index + 1}
            </button>
          ))}

          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </button>

        </div>
      )}

    </div>
  );
}

export default Anomalies;