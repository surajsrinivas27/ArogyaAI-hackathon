import { FaBell, FaMoon, FaUserCircle } from "react-icons/fa";
import "./../styles/dashboard.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        🩺 <span>ArogyaAI</span>
      </div>

      <div className="nav-right">
        <FaBell className="icon" />
        <FaMoon className="icon" />
        <FaUserCircle className="icon profile" />
      </div>
    </nav>
  );
}

export default Navbar;