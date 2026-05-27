import React from "react";

import {
  LayoutDashboard,
  BrainCircuit,
  TriangleAlert,
  Search,
  CalendarDays,
  UserCircle2,
  Cpu
} from "lucide-react";

import {
  Link,
  useLocation
} from "react-router-dom";

function Navbar() {

  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path;

  return (
    <nav className="navbar">

      {/* LEFT */}
      <div className="navbar-left">

        <Link to="/" className="navbar-logo">

          <div className="logo-icon">
            <Cpu size={22} />
          </div>

          <div className="logo-text">
            <h2>Cost Intelligence</h2>
            <span>AI Cloud Monitoring</span>
          </div>

        </Link>

      </div>

      {/* CENTER */}
      <div className="navbar-center">

        <Link
          to="/"
          className={`nav-link ${isActive("/") ? "active" : ""}`}
        >
          {/* <LayoutDashboard size={18} /> */}
          Dashboard
        </Link>

        <Link
          to="/insights"
          className={`nav-link ${isActive("/insights") ? "active" : ""}`}
        >
          {/* <BrainCircuit size={18} /> */}
          Insights
        </Link>

        <Link
          to="/anomalies"
          className={`nav-link ${isActive("/anomalies") ? "active" : ""}`}
        >
          {/* <TriangleAlert size={18} /> */}
          Anomalies
        </Link>

      </div>

      {/* RIGHT */}
      <div className="navbar-right">

        <div className="search-box">

          <Search
            size={18}
            className="search-icon"
          />

          <input
            type="text"
            placeholder="Search services, insights..."
          />

        </div>

        <div className="time-filter-wrapper">

          <CalendarDays
            size={18}
            className="calendar-icon"
          />

          <select className="time-select">
            <option>Last 7 Days</option>
            <option>Last 30 Days</option>
            <option>Last 90 Days</option>
            <option>Last Year</option>
          </select>

        </div>

        <div className="profile-avatar">
          <UserCircle2 size={22} />
        </div>

      </div>

    </nav>
  );
}

export default Navbar;