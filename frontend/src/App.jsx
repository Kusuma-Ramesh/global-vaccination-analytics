import { Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import Sidebar from "./components/Sidebar.jsx";
import PageTransition from "./components/PageTransition.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import CoverageExplorer from "./pages/CoverageExplorer.jsx";
import DiseaseExplorer from "./pages/DiseaseExplorer.jsx";
import VaccineIntroduction from "./pages/VaccineIntroduction.jsx";
import Correlation from "./pages/Correlation.jsx";

export default function App() {
  const location = useLocation();

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <Sidebar />
      <main className="main" id="main-content">
        <AnimatePresence mode="wait">
          <PageTransition key={location.pathname}>
            <Routes location={location}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/coverage" element={<CoverageExplorer />} />
              <Route path="/disease" element={<DiseaseExplorer />} />
              <Route path="/introduction" element={<VaccineIntroduction />} />
              <Route path="/correlation" element={<Correlation />} />
            </Routes>
          </PageTransition>
        </AnimatePresence>
      </main>
    </div>
  );
}
