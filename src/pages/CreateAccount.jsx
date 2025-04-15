import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

export function CreateAccount() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { signIn } = useAuth(); // bring in global auth

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (form.username.length < 3) {
      setError("Username must be at least 3 characters long.");
      return;
    }

    if (form.password.length < 10) {
      setError("Password must be at least 10 characters long.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(form.email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setError(""); // clear old errors

    try {
      // Post to backend
      const response = await axios.post("http://localhost:8000/signup", form);

      // On success, update global auth and go to /home
      const userData = response.data; // adjust if backend returns { user: {...} }
      signIn(userData);
      navigate("/home");

    } catch (err) {
      console.error(err);
      setError("Could not create account. Try again.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900 text-white px-4 font-mono">
      <Link to="/" className="mb-2 text-2xl font-bold font-mono text-white hover:text-slate-300">
        Detect the Deepfake
      </Link>
      <div className="fixed bottom-0 bg-transparent text-white p-2 flex justify-center z-50">
        <button onClick={() => navigate("/")} title="Home" className="p-2 semi-rounded-full bg-transparent hover:bg-slate-700">
          <span className="material-icons">home</span>
        </button>
      </div>
      
      <div className="bg-slate-800 p-6 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-xl mb-4 text-center">Create Account</h2>
        
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">

          <div>
            <label htmlFor="firstName" className="block mb-1">First Name</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              className="w-full px-3 py-2 rounded bg-slate-700 text-white"
              value={form.firstName}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="lastName" className="block mb-1">Last Name</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              className="w-full px-3 py-2 rounded bg-slate-700 text-white"
              value={form.lastName}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="email" className="block mb-1">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="w-full px-3 py-2 rounded bg-slate-700 text-white"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="username" className="block mb-1">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              className="w-full px-3 py-2 rounded bg-slate-700 text-white"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block mb-1">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              className="w-full px-3 py-2 rounded bg-slate-700 text-white"
              value={form.password}
              onChange={handleChange}
              required
            />
            {error && <p className="text-red-400 text-sm mt-1">{error}</p>}
          </div>

          <button
            type="submit"
            className="bg-indigo-700 hover:bg-indigo-600 text-white p-2 rounded"
          >
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}
