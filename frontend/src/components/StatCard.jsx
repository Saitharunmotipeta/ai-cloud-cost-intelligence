import React from "react";

import {
  AlertTriangle,
  BrainCircuit,
  Activity,
  ServerCrash
} from "lucide-react";

import SkeletonCard from "./skeletons/SkeletonCard";

function StatCard({
  title,
  value,
  color = "blue",
  loading = false
}) {

  const cardConfig = {

    blue: {
      className: "stat-card-blue",
      icon: <BrainCircuit size={22} />
    },

    red: {
      className: "stat-card-red",
      icon: <AlertTriangle size={22} />
    },

    green: {
      className: "stat-card-green",
      icon: <Activity size={22} />
    },

    yellow: {
      className: "stat-card-yellow",
      icon: <ServerCrash size={22} />
    }

  };

  if (loading) {
    return <SkeletonCard />;
  }

  return (

    <div className={`modern-stat-card ${cardConfig[color].className}`}>

      {/* GLOW */}
      <div className="card-glow"></div>

      {/* TOP */}
      <div className="card-header">

        <div className="stat-icon">
          {cardConfig[color].icon}
        </div>

        <span className="stat-title">
          {title}
        </span>

      </div>

      {/* VALUE */}
      <div className="card-value">
        {value ?? 0}
      </div>

      {/* FOOTER */}
      <div className="card-footer">
        <span className="trend-positive">
          ↑ Live Monitoring
        </span>
      </div>

    </div>

  );
}

export default StatCard;