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

  // 🔥 ONLY light filtering (backend already filtered)
  const filteredAnomalies = anomalies.filter((a) => {

    const matchSeverity =
      selectedSeverity === "ALL" || a.severity === selectedSeverity;

    const matchDate =
      !selectedDate || a.timestamp?.startsWith(selectedDate);

    return matchSeverity && matchDate;
  });

  return (
    <div className="anomalies">
      <h1>Cost Anomalies</h1>

      {/* 🔥 FILTERS */}
      <div className="filters">
        <select
          value={selectedSeverity}
          onChange={(e) => setSelectedSeverity(e.target.value)}
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
          onChange={(e) => setSelectedDate(e.target.value)}
        />
      </div>

      <AnomalyTable
        anomalies={filteredAnomalies}
        loading={loading}
        error={error}
      />
    </div>
  );
}

export default Anomalies;