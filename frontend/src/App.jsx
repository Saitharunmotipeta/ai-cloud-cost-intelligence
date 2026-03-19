import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainLayout from "./layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";

function App() {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/insights" element={<Insights />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;