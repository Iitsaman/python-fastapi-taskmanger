import { useState } from "react";
import { api, setToken } from "../api";

export default function Auth({ onLogin, setIsAdmin }) {
  // Register state
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");

  // Login state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Email validation
  const isValidEmail = (email) => /\S+@\S+\.\S+/.test(email);

  // Register
  const register = async () => {
    if (!regEmail || !regPassword) {
      alert("Please fill all register fields");
      return;
    }

    if (!isValidEmail(regEmail)) {
      alert("Invalid email format");
      return;
    }

    try {
      const res = await api.post("/auth/register", {
        email: regEmail,
        password: regPassword,
      });

      alert(res.data.detail || "Registered successfully!");

      // clear fields
      setRegEmail("");
      setRegPassword("");

      // optional: auto login logic here
    } catch (err) {
      console.error(err.response?.data);
      alert(
        err.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : "Registration failed"
      );
    }
  };

  // Login

const login = async () => {
  if (!loginEmail || !loginPassword) {
    alert("Enter email and password");
    return;
  }

  try {
    const formData = new URLSearchParams();
    formData.append("username", loginEmail); // ⚠️ important
    formData.append("password", loginPassword);

    const res = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    const token = res.data.access_token;
    const role = res.data.role;

    if (token) {
      localStorage.setItem("token", token);
      setToken(token);
      onLogin(token);
      if (role === "admin") setIsAdmin(true);
    }
  } catch (err) {
    console.log("ERROR:", err.response?.data);
    alert("Login failed");
  }
};

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Register</h2>
      <input
        type="email"
        placeholder="Email"
        value={regEmail}
        onChange={(e) => setRegEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={regPassword}
        onChange={(e) => setRegPassword(e.target.value)}
      />
      <button onClick={register}>Register</button>

      <hr />

      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={loginEmail}
        onChange={(e) => setLoginEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={loginPassword}
        onChange={(e) => setLoginPassword(e.target.value)}
      />
      <button onClick={login}>Login</button>
    </div>
  );
}