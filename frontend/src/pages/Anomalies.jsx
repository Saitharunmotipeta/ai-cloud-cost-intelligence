import React from "react";
import { useAnomalies } from "../hooks/useAnomalies";
import AnomalyTable from "../components/AnomalyTable";

function Anomalies() {
  const { anomalies, loading, error } = useAnomalies();
//   const loading = true;

  return (
    <div className="anomalies">
      <h1>Cost Anomalies</h1>

      <AnomalyTable
        anomalies={anomalies}
        loading={loading}
        error={error}
      />
    </div>
  );
}

export default Anomalies;