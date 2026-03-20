import { useState } from "react";
import Navbar from "../components/Navbar";

const MainLayout = ({ children }) => {
  const [timeRange, setTimeRange] = useState("7d");

  return (
    <div className="app-container">
      <Navbar />

      {/* 🔥 GLOBAL HEADER */}
      <div className="top-bar">
        <h2 className="page-title">Cloud Cost Dashboard</h2>

        <select
          className="time-filter"
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
        >
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
        </select>
      </div>

      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;