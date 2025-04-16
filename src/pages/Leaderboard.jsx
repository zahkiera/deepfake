import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

{/* This page establishes the leaderboard.  */}

export function Leaderboard() {
  {/* Variables */}
  const [leaders, setLeaders] = useState([])

  {/* Communicate with backend to find top players */}
  useEffect(() => {
    const fetchLeaders = async () => {
      try {
        const res = await axios.get('http://localhost:8000/leaderboard')
        setLeaders(res.data)
      } catch (err) {
        console.error('Failed to fetch leaderboard:', err)
      }
    }
    fetchLeaders()
  }, [])

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 flex flex-col items-center"> {/* Page contianer */}
      <Link to="/" className="text-2xl font-bold mb-6 font-mono text-white hover:text-slate-300"> {/* Title that can take the user to the homepage */}
        Deepfake Detector
      </Link>
      
      <h2 className="text-xl mb-4 font-mono">Top 5 Players</h2>

      <div className="w-full max-w-md bg-slate-800 rounded-xl p-4 shadow-lg"> {/* Leaderboard container */}
        {leaders.length === 0 ? (
          <p className="text-center text-gray-400 font-mono">No scores yet!</p>
        ) : (
          <table className="w-full text-left"> {/* Display names and high scores in a table format */}
            <thead>
              <tr className="border-b border-slate-600">
                <th className="py-2 font-mono">Username</th>
                <th className="py-2 text-right font-mono">High Score</th>
              </tr>
            </thead>
            <tbody> 
              {leaders.map((user, idx) => (
                <tr key={idx} className="border-b border-slate-700">
                  <td className="py-2">{user.username}</td>
                  <td className="py-2 text-right">{user.high_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

