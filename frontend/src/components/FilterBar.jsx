import React from "react";

import { Filter } from "lucide-react";

export default function FilterBar({
  filters,
  setFilters
}) {

  return (

    <div className="modern-filter-bar">

      <div className="filter-group">

        <div className="filter-icon">
          <Filter size={16} />
        </div>

        <select
          className="modern-select"
          value={filters.severity}
          onChange={(e) =>
            setFilters({
              ...filters,
              severity: e.target.value
            })
          }
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

    </div>

  );
}