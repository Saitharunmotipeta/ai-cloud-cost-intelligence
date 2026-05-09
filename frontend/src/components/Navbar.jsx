import React from 'react'
import { Link, useLocation } from 'react-router-dom'

function Navbar({ sidebarOpen, setSidebarOpen }) {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? '✕' : '☰'}
          </button>

          <Link to="/" className="navbar-logo">
            <div className="logo-icon">💰</div>
            <span>Cost Intelligence</span>
          </Link>
        </div>

        <div className="navbar-center">
          <Link
            to="/"
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
          >
            Dashboard
          </Link>

          <Link
            to="/insights"
            className={`nav-link ${isActive('/insights') ? 'active' : ''}`}
          >
            Insights
          </Link>

          <Link
            to="/anomalies"
            className={`nav-link ${isActive('/anomalies') ? 'active' : ''}`}
          >
            Anomalies
          </Link>

          <Link
            to="/about"
            className={`nav-link ${isActive('/about') ? 'active' : ''}`}
          >
            About Project
          </Link>
        </div>

        <div className="navbar-right">
          <div className="user-menu">
            <span className="user-icon">👤</span>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar