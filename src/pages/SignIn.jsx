import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/signin", {
        email,
        password,
      });

      // Get user data from response and update global auth
      const userData = response.data; // adjust if response is { user: {...} }
      signIn(userData); // this updates global state

      navigate("/home"); 
    } catch (err) {
      console.error(err);
      setError("Invalid login credentials");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900 text-white px-4 font-mono">
      {/* Fixed bottom nav */}
      <div className="fixed bottom-0 w-full bg-slate-900 text-white p-2 flex justify-center z-50">
        <button onClick={() => navigate("/")} title="Home" className="p-2 semi-rounded-full bg-slate-900 hover:bg-slate-700">
          <span className="material-icons">home</span>
        </button>
      </div>

      {/* Title */}
      <Link to="/" className="mb-6 text-2xl font-bold font-mono text-white hover:text-slate-300">
        Detect the Deepfake
      </Link>

      {/* Sign-in form */}
      <div className="bg-slate-800 p-6 rounded-lg shadow-md w-full max-w-md">
        <form onSubmit={handleSignIn} className="bg-slate-800 p-8 rounded space-y-4">
          <h2 className="text-xl text-center">Welcome Back</h2>

          <input
            type="email"
            placeholder="Email"
            className="w-full p-2 rounded text-black"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-2 rounded text-black"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className="w-full bg-indigo-700 hover:bg-indigo-600 text-white p-2 rounded">
            Sign In
          </button>

          {error && <p className="text-red-400 text-sm text-center">{error}</p>}
        </form>
      </div>
    </div>
  );
}
