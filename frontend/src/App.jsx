import { useState, useEffect } from "react";
import Auth from "./components/Auth";
import Tasks from "./components/Tasks";
import AdminTasks from "./components/Admintasks";
import { api, setToken } from "./api"; 

function App() {
  const [token, setTokenState] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  // Restore token and role on mount
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setTokenState(savedToken);
      setToken(savedToken); 

      // Fetch user info to restore role
      api.get("/auth/me")
        .then((res) => {
          if (res.data.role === "admin") setIsAdmin(true);
        })
        .catch(() => {
          // token invalid, logout
          setTokenState("");
          setIsAdmin(false);
          localStorage.removeItem("token");
        });
    }
  }, []);

  // Called after login
  const handleLogin = (token) => {
    setTokenState(token);
    setToken(token); 

    // Fetch user role immediately
    api.get("/auth/me")
      .then((res) => {
        if (res.data.role === "admin") setIsAdmin(true);
      })
      .catch(() => setIsAdmin(false));
  };

  const handleLogout = () => {
    setTokenState("");
    setIsAdmin(false);
    localStorage.removeItem("token");
    setToken(""); //
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Task Manager</h1>
      
      {!token && <Auth onLogin={handleLogin} setIsAdmin={setIsAdmin} />}
      
      {token && <Tasks onLogout={handleLogout} isAdmin={isAdmin} />}
      
      {token && isAdmin && <AdminTasks />}
    </div>
  );
}

export default App;