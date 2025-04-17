import { createContext, useContext, useState, useEffect } from "react";

{/* This file handles global authentication */}

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState("") // You can optionally initialize from localStorage
  const [loading, setLoading] = useState(true);


  const signIn = (userData) => {
    setUser(userData)
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const signOut = () => {
    setUser("")
    localStorage.removeItem("user");
  };

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if(savedUser !== "undefined"){
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  return (
    <AuthContext.Provider value={{ user, signIn, signOut, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  return useContext(AuthContext)
}
