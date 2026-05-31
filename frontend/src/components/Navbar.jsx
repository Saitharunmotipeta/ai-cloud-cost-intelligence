import React, {
  useState,
  useEffect,
  useRef
} from "react";

import {
  UserCircle2,
  Cpu,
  ShieldCheck,
  Globe,
  Sparkles
} from "lucide-react";

import {
  Link,
  useLocation
} from "react-router-dom";

function Navbar() {

  const location = useLocation();

  const dropdownRef = useRef(null);

  const [profileOpen, setProfileOpen] =
    useState(false);

  const accountId =
    localStorage.getItem("account_id");

  const isActive = (path) =>
    location.pathname === path;

  /* =========================
     CLOSE DROPDOWN
  ========================= */

  useEffect(() => {

    function handleClickOutside(event) {

      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setProfileOpen(false);
      }

    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {

      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

    };

  }, []);

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

        <div
          className="profile-wrapper"
          ref={dropdownRef}
        >

          {/* AVATAR */}

          <div
            className="profile-avatar"
            onClick={() =>
              setProfileOpen(!profileOpen)
            }
          >

            <UserCircle2 size={22} />

          </div>

          {/* DROPDOWN */}

          {profileOpen && (

            <div className="profile-dropdown">

              {/* TOP */}

              <div className="profile-top">

                <div className="profile-big-avatar">

                  <UserCircle2 size={42} />

                </div>

                <div>

                  <h3>
                    Saitharun
                  </h3>

                  <span>
                    AI Cloud Architect
                  </span>

                </div>

              </div>

              {/* STATUS */}

              <div className="profile-status">

                <div className="status-dot"></div>

                <span>
                  Monitoring Active
                </span>

              </div>

              {/* INFO */}

              <div className="profile-info-grid">

                <div className="profile-info-card">

                  <ShieldCheck size={16} />

                  <div>

                    <label>
                      Account ID
                    </label>

                    <p>
                      {accountId || "N/A"}
                    </p>

                  </div>

                </div>

                <div className="profile-info-card">

                  <Globe size={16} />

                  <div>

                    <label>
                      Region
                    </label>

                    <p>
                      eu-north-1
                    </p>

                  </div>

                </div>

                <div className="profile-info-card">

                  <Sparkles size={16} />

                  <div>

                    <label>
                      Environment
                    </label>

                    <p>
                      Production
                    </p>

                  </div>

                </div>

              </div>

              {/* FOOTER */}

              <div className="profile-footer">

                Enterprise AI Monitoring Suite

              </div>

            </div>

          )}

        </div>

      </div>

    </nav>

  );
}

export default Navbar;