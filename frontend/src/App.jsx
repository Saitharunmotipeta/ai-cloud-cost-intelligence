import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainLayout from "./layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Anomalies from "./pages/Anomalies";
import AboutProject from './pages/AboutProject';

function App() {

  // 🔥 TEMP HARDCODE (SAFE + CLEAN)
  const ACCOUNT_ID = "11111111-1111-1111-1111-111111111111";

  // set only once
  if (!localStorage.getItem("account_id")) {
    localStorage.setItem("account_id", ACCOUNT_ID);
  }

  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/anomalies" element={<Anomalies />} />
          <Route path="/about" element={<AboutProject />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;