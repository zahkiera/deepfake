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
Open a new folder in VS Code and type:
```bash
git init
git clone https://github.com/ZainaK05/Secure-Software-Final-Project.git 
```

### 2. Backend Setup
#### Install Python packages

```bash
python -m venv venv # (or py -m venv venv)
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate (make sure you're in the parent directory of your venv folder when trying to activate it)
pip install -r requirements.txt
```

#### Run FastAPI Server
```bash
cd Secure-Software-Final-Project
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup
Open a new terminal
```bash
cd Secure-Software-Final-Project
cd frontend
npm install
npm run dev
```
The link will pop up in the terminal, crtl+click to navigate to the game !

**Make sure the backend is running at http:// 127.0.0.1:8000 and frontend at http:// localhost:5173.**
