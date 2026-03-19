import Navbar from "../components/Navbar";

const MainLayout = ({ children }) => {
  return (
    <div className="app-container">
      <Navbar />
      <main style={{ padding: "20px" }}>
        {children}
      </main>
    </div>
  );
};

export default MainLayout;