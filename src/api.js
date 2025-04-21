const API_BASE_URL = "http://127.0.0.1:8000/api";  // Change when/if we deploy

// Register a new user
export async function registerUser(username, password, firstName, lastName, email) {
  const res = await fetch(`${API_BASE_URL}/user/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password, firstName, lastName, email }),
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

export async function submitAnswer(data){
  const res = await fetch("http://127.0.0.1:8000/api/game/submit",{
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

export async function getLeaderboard(limit = 10) {
  const res = await fetch(`http://127.0.0.1:8000/api/leaderboard?limit=${limit}`);
  return await res.json();
}

export async function submitScore(user_id, score){
  const res = await fetch(`${API_BASE_URL}/leaderboard/submit_score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, score }),
  });

  return await res.json();
}

export async function getQuestionMedia(questionId) {
  const res = await fetch(`${API_BASE_URL}/media/${questionId}`);
  return await res.json();
}

export function getFullMediaUrl(mediaPath) {
  console.log(`http://localhost:8000/media/${mediaPath}`)
  return `http://localhost:8000/media/${mediaPath}`;
}
