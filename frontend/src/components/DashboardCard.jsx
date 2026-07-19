import { motion } from "framer-motion";

function DashboardCard({ title, value, icon }) {
  return (
    <motion.div
      whileHover={{
        scale: 1.05,
        y: -8,
      }}
      className="dashboard-card"
    >
      <div className="card-icon">{icon}</div>

      <h3>{title}</h3>

      <h1>{value}</h1>
    </motion.div>
  );
}

export default DashboardCard;