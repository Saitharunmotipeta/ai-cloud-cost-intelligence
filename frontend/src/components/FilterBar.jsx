import React from "react";

export default function FilterBar({ filters, setFilters, services }) {

  return (
    <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>

      {/* Severity */}
      <select
        value={filters.severity}
        onChange={(e) =>
          setFilters({ ...filters, severity: e.target.value })
        }
      >
        <option value="">All Severity</option>
        <option value="CRITICAL">Critical</option>
        <option value="HIGH">High</option>
        <option value="MEDIUM">Medium</option>
        <option value="LOW">Low</option>
      </select>

      {/* Service */}
      <select
        value={filters.service}
        onChange={(e) =>
          setFilters({ ...filters, service: e.target.value })
        }
      >
        <option value="">All Services</option>
        {services.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>

    </div>
  );
}