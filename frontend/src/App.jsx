import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainLayout from "./layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Anomalies from "./pages/Anomalies";

function App() {
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