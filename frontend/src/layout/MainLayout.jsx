import Navbar from "../components/Navbar";

const MainLayout = ({ children }) => {

  return (
    <div className="layout-wrapper">

      <Navbar />

      <main className="main-wrapper">

        <div className="main-content">
          {children}
        </div>

      </main>

    </div>
  );
};

export default MainLayout;