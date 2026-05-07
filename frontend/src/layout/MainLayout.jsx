import { useState } from "react";
import Navbar from "../components/Navbar";

const MainLayout = ({ children }) => {
  const [timeRange, setTimeRange] = useState("7d");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="layout-wrapper">
      <Navbar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <div className="layout-content">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
          <nav className="sidebar-nav">
            <div className="sidebar-section">
              <h3 className="sidebar-title">Dashboard</h3>
              <a href="/" className="sidebar-link active">Overview</a>
              <a href="/insights" className="sidebar-link">Insights</a>
              <a href="/anomalies" className="sidebar-link">Anomalies</a>
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="main-wrapper">
          <div className="header-section">
            <div className="header-left">
              <h1 className="page-title">Cloud Cost Intelligence</h1>
              <p className="page-subtitle">Monitor and optimize your cloud spending</p>
            </div>

            <div className="header-right">
              <div className="time-range-selector">
                <label htmlFor="timeRange" className="filter-label">Time Period</label>
                <select
                  id="timeRange"
                  className="time-filter"
                  value={timeRange}
                  onChange={(e) => setTimeRange(e.target.value)}
                >
                  <option value="7d">Last 7 Days</option>
                  <option value="30d">Last 30 Days</option>
                  <option value="90d">Last 90 Days</option>
                  <option value="1y">Last Year</option>
                </select>
              </div>
            </div>
          </div>

          <div className="main-content">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;