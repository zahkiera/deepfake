const API_BASE_URL = "http://127.0.0.1:8000/api";  // Change when/if we deploy

// Register a new user
export async function registerUser(username, password) {
  const res = await fetch(`${API_BASE_URL}/user/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return await res.json();
}

// Log in user
export async function loginUser(username, password) {
  const res = await fetch(`${API_BASE_URL}/user/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return await res.json();
}

// Get specific question by ID 
export async function getQuestion(questionId) {
  const res = await fetch(`${API_BASE_URL}/game/${questionId}`);
  return await res.json();
}

// Get a random question
export async function getRandomQuestion() {
  const res = await fetch(`${API_BASE_URL}/game/random`);
  return await res.json();
}
