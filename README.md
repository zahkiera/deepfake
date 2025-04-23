# Deepfake Detection Game

A full stack educational game that helps users learn how to detect deepfake images. Built with **React** for the frontend and **FastAPI** for the backend

## Features

- User signup, login, and account deactivation
- Game mode where users select which image is a deepfake
- Score tracking and leaderboard
- Image/media management

## Technologies Used

**Frontend:**
- React
- JavaScript
- Vite
- Axios
- Tailwind CSS

**Backend:**
- FastAPI
- SQLite
- Uvicorn
- Pydantic
- Python
- Passlib

**Other:**
- CORS Middleware
- Global authentication

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ZainaK05/Secure-Software-Final-Project.git 
```

### 2. Backend Setup
#### Install Python packages

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run FastAPI Server
```bash
cd Secure-Software-Final-Project
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
Open a new terminal
npm install
npm run dev
```
**Make sure the backend is running at http:// 127.0.0.1:8000 and frontend at http:// localhost:5173.**
