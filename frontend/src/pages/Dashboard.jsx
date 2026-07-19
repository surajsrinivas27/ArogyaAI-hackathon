import { useEffect, useState } from "react";
import {
  FaHeartbeat,
  FaFileMedical,
  FaExclamationTriangle,
  FaUpload,
} from "react-icons/fa";

import Navbar from "../components/Navbar";
import DashboardCard from "../components/DashboardCard";
import Loader from "../components/Loader";

import api from "../services/api";
import "../styles/dashboard.css";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get("/reports/dashboard", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setDashboard(response.data);
    } catch (err) {
      console.log(err);
    }
  };

  if (!dashboard) return <Loader />;

  return (
    <div className="dashboard">

      <Navbar />

      <div className="dashboard-hero">

        <div>

          <h1>
            👋 Welcome Back
          </h1>

          <p>
            AI-powered healthcare monitoring for you and your family.
          </p>

        </div>

        <button
          className="uploadBtn"
          onClick={() => window.location.href="/upload"}
        >
          <FaUpload />

          Upload Report
        </button>

      </div>

      <div className="cards">

        <DashboardCard
          title="Health Score"
          value={dashboard.average_health_score}
          icon={<FaHeartbeat />}
        />

        <DashboardCard
          title="Reports"
          value={dashboard.total_reports}
          icon={<FaFileMedical />}
        />

        <DashboardCard
          title="Abnormal"
          value={dashboard.abnormal_reports}
          icon={<FaExclamationTriangle />}
        />

      </div>

    </div>
  );
}

export default Dashboard;