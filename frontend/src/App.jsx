import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainLayout from "./layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Anomalies from "./pages/Anomalies";

function App() {

  // 🔥 TEMP HARDCODE (SAFE + CLEAN)
  const ACCOUNT_ID = "123e4567-e89b-12d3-a456-426614174000";

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
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;