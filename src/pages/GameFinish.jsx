import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";

export function GameFinish() {
  const location = useLocation()
  const score = location.state?.score || 0;
  const str = "You have a good eye!"
  const str2 = "How about another try?"
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900 text-white px-4 font-mono">
        <h2 className="text-2xl mb-3">Game Over</h2>
       
        {score >= 80 ? (
          <p>{str}</p>) : (
          <p>{str2}</p>
          )}
        <p className="mb-3">Score: {score}</p>

        <Link to="/play" className="px-4 py-2 bg-slate-900 text-white rounded hover:bg-slate-800 hover:text-white">
Play Again</Link>

        <Link to="/leaderboard" className="px-4 py-2 bg-slate-900 text-white rounded hover:bg-slate-800 hover:text-white">
View Leaderboard</Link>
    

      </div>

      
    );
  }
  