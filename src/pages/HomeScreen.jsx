import { Link } from "react-router-dom";

export function HomeScreen() {
    return(
      <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900 text-white px-4 font-mono">
            <h2 className="text-2xl font-mono font-bold">Detect the Deepfake</h2>
                       
<Link to="/play" className="px-4 py-2 bg-slate-900 text-white rounded hover:bg-slate-800 hover:text-white">
  Start Game
</Link>

<Link to="/leaderboard" className="px-4 py-2 bg-slate-900 text-white rounded hover:bg-slate-800 hover:text-white">
  View Leaderboard
</Link>

<Link to="/tutorial" className="px-4 py-2 bg-slate-900 text-white rounded hover:bg-slate-800 hover:text-white">
Tutorial
</Link> 

        </div>
    );
}