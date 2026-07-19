import { useState } from "react";
import api from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

        const response = await api.post("/auth/login", formData, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        });

        localStorage.setItem(
  "token",
  response.data.access_token
);

        alert("Login Successful!");

        window.location.href = "/dashboard";

        console.log(localStorage.getItem("token"));

    } catch (error) {
        console.log(error);

        alert("Invalid Email or Password");
    }
    };
  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f4f7fc",
      }}
    >
      <div
        style={{
          width: "350px",
          background: "white",
          padding: "30px",
          borderRadius: "15px",
          boxShadow: "0px 5px 15px rgba(0,0,0,0.15)",
        }}
      >
        <h1 style={{ textAlign: "center" }}>🩺 ArogyaAI</h1>

        <p
          style={{
            textAlign: "center",
            color: "gray",
            marginBottom: "20px",
          }}
        >
          AI Healthcare Assistant
        </p>

       <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
                width: "100%",
                padding: "10px",
                marginBottom: "15px",
                boxSizing: "border-box",
            }}
            />

       <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
                width: "100%",
                padding: "10px",
                marginBottom: "20px",
                boxSizing: "border-box",
            }}
            />

        <button
          onClick={handleLogin}
          style={{
            width: "100%",
            padding: "12px",
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "16px",
            
          }}
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;