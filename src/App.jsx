import { Route, Routes } from 'react-router-dom'
import { CreateAccount } from './pages/CreateAccount'
import { GameFinish } from './pages/GameFinish'
import { GameScreen } from './pages/GameScreen'
import { HomeScreen } from './pages/HomeScreen'
import { Leaderboard } from './pages/Leaderboard'
import { Settings } from './pages/Settings'
import { SignIn } from './pages/SignIn'
import { Welcome } from './pages/Welcome'
import { Tutorial } from './pages/Tutorial'

import { Runner } from './components/Runner'
import { AuthProvider } from './context/AuthContext'



function App() {
  return (
    <div>
      <Runner />
      <main>
        <AuthProvider>
        <Routes> 
          <Route path="/" element={<Welcome />} />
          <Route path="/sign-up" element={<CreateAccount />} />
          <Route path="/play" element={<GameScreen />} /> 
          <Route path="/fin" element={<GameFinish />} />
          <Route path="/home" element={<HomeScreen />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/sign-in" element={<SignIn />} />
          <Route path="/tutorial" element={<Tutorial />} />
        </Routes>
        </AuthProvider>
      </main>
    </div>
  )
}

export default App
