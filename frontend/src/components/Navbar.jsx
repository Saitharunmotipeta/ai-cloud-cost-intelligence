import React from 'react'
import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="nav-container">

        <Link to="/" className="nav-logo">
          AI Cloud Cost Intelligence
        </Link>

        <div className="nav-links">
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
        </div>
      </div>
    </nav>
  )
}

export default Navbar