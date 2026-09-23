import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

const links = [
  { to: "/", label: "Global Overview", end: true },
  { to: "/coverage", label: "Coverage Explorer" },
  { to: "/disease", label: "Disease Trends" },
  { to: "/introduction", label: "Vaccine Rollout" },
  { to: "/correlation", label: "Coverage vs. Disease" },
];

function BrandMark() {
  return (
    <div className="brand-mark" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
        <path d="M12 3v18M4.5 8.5c2 1.4 3.2 1.4 5.2 0M4.5 15.5c2-1.4 3.2-1.4 5.2 0M18.5 8.5c-2 1.4-3.2 1.4-5.2 0M18.5 15.5c-2-1.4-3.2-1.4-5.2 0" />
      </svg>
    </div>
  );
}

function NavList({ onNavigate }) {
  return (
    <nav aria-label="Primary">
      {links.map((l) => (
        <NavLink
          key={l.to}
          to={l.to}
          end={l.end}
          onClick={onNavigate}
          className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}
        >
          {l.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default function Sidebar() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Close the mobile drawer whenever the route changes.
  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <>
      <div className="nav-toggle">
        <button
          type="button"
          aria-expanded={open}
          aria-controls="primary-sidebar"
          aria-label={open ? "Close navigation menu" : "Open navigation menu"}
          onClick={() => setOpen((v) => !v)}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {open ? <path d="M6 6l12 12M18 6l-12 12" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
        <span>Vaccination Intelligence</span>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            className="nav-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.18 }}
            onClick={() => setOpen(false)}
          />
        )}
      </AnimatePresence>

      <aside id="primary-sidebar" className={"sidebar" + (open ? " open" : "")}>
        <div className="brand">
          <BrandMark />
          <div>
            <div className="brand-title">Vaccination Intelligence</div>
            <div className="brand-sub">Global Immunization Surveillance</div>
          </div>
        </div>

        <NavList onNavigate={() => setOpen(false)} />

        <div className="sidebar-foot">
          Data sourced from WHO / UNICEF WUENIC estimates.
        </div>
      </aside>
    </>
  );
}
