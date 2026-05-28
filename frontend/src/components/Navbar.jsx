import React from "react";

import {
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

        <Link
          to="/"
          className="navbar-logo"
        >

          <div className="logo-icon">
            <Cpu size={22} />
          </div>

          <div className="logo-text">

            <h2>
              Cost Intelligence
            </h2>

            <span>
              AI Cloud Monitoring
            </span>

          </div>

        </Link>

      </div>

      {/* CENTER */}

      <div className="navbar-center">

        <Link
          to="/"
          className={`nav-link ${isActive("/") ? "active" : ""}`}
        >
          Dashboard
        </Link>

        <Link
          to="/insights"
          className={`nav-link ${isActive("/insights") ? "active" : ""}`}
        >
          Insights
        </Link>

        <Link
          to="/anomalies"
          className={`nav-link ${isActive("/anomalies") ? "active" : ""}`}
        >
          Anomalies
        </Link>

        <Link
          to="/about"
          className={`nav-link ${isActive("/about") ? "active" : ""}`}
        >
          About Project
        </Link>

        <Link
          to="/architecture"
          className={`nav-link ${isActive("/architecture") ? "active" : ""}`}
        >
          Architecture
        </Link>

      </div>

      {/* RIGHT */}

      <div className="navbar-right">

        {/* SEARCH */}

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

        {/* TIME FILTER */}

        <div className="time-filter-wrapper">

          <CalendarDays
            size={18}
            className="calendar-icon"
          />

          <select className="time-select">

            <option>
              Last 7 Days
            </option>

            <option>
              Last 30 Days
            </option>

            <option>
              Last 90 Days
            </option>

            <option>
              Last Year
            </option>

          </select>

        </div>

        {/* PROFILE */}

        <div className="profile-avatar">
          <UserCircle2 size={22} />
        </div>

      </div>

    </nav>

  );
}

export default Navbar;