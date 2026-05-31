import React, { useState } from "react";

import {
  ShieldAlert,
  Sparkles
} from "lucide-react";

import SkeletonTable from "./skeletons/SkeletonTable";

function InsightTable({
  insights = [],
  loading = false,
  error = null,
  newIds = new Set(),
  itemsPerPage = 3
}) {

  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(
    insights.length / itemsPerPage
  );

  const startIndex =
    (currentPage - 1) * itemsPerPage;

  const currentInsights =
    insights.slice(
      startIndex,
      startIndex + itemsPerPage
    );

  const getSeverityClass = (severity) => {

    switch (severity) {

      case "CRITICAL":
        return "severity-critical";

      case "HIGH":
        return "severity-high";

      case "MEDIUM":
        return "severity-medium";

      case "LOW":
        return "severity-low";

      default:
        return "";
    }

  };

  if (loading) {
    return (
      <SkeletonTable
        rows={itemsPerPage}
      />
    );
  }

  if (error && insights.length === 0) {
    return (
      <div className="table-error">
        Failed to load insights
      </div>
    );
  }

  if (!insights.length) {
    return (
      <div className="empty-state">
        No insights available
      </div>
    );
  }

  return (

    <div className="modern-table-wrapper">

      {/* <div className="table-header">

        <h2>
          Latest AI Insights
        </h2>

        <a
          href="/insights"
          className="view-all-link"
        >
          View All →
        </a>

      </div> */}

      <div className="table-scroll">

        <table className="modern-table">

          <thead>

            <tr>
              <th>Service</th>
              <th>Severity</th>
              <th>Explanation</th>
              <th>Recommendation</th>
            </tr>

          </thead>

          <tbody>

            {currentInsights.map((insight, index) => (

              <tr
                key={
                  insight.id ||
                  `${insight.service}-${index}`
                }
              >

                {/* SERVICE */}

                <td>

                  <div className="service-cell">

                    <div className="service-icon">
                      <Sparkles size={15} />
                    </div>

                    <span>
                      {insight.service}
                    </span>

                  </div>

                </td>

                {/* SEVERITY */}

                <td>

                  <div
                    className={`severity-pill ${getSeverityClass(insight.severity)}`}
                  >

                    <ShieldAlert size={13} />

                    {insight.severity}

                  </div>

                </td>

                {/* EXPLANATION */}

                <td className="table-text">

                  {newIds.has(insight.id) && (
                    <span className="new-badge">
                      NEW
                    </span>
                  )}

                  {
                    insight.explanation ||
                    insight.message
                  }

                </td>

                {/* ACTION */}

                <td className="table-text">

                  {
                    insight.action ||
                    insight.recommendation
                  }

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {/* PAGINATION */}

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

export default InsightTable;