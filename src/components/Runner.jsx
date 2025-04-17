import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; 

export function Runner() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { user, signOut } = useAuth();
  
  // Hide Runner on specific pages
  const hideOnPaths = ["/", "/sign-in", "/sign-up"];
  if (hideOnPaths.includes(location.pathname)) return null;

  const handleLogout = () => {
    signOut()
    navigate("/");
  };

  return (
    <div className="fixed bottom-0 left-0 w-full bg-slate-900 text-white p-2 flex justify-center gap-8 z-50">
      <button onClick={() => navigate("/settings")} title="Settings" className="p-2 semi-rounded-full bg-slate-900 hover:bg-slate-700">
        <span className="material-icons align-middle">settings</span>
      </button>
      
      
      <button onClick={() => navigate("/home")} title="Home" className="p-2 semi-rounded-full bg-slate-900 hover:bg-slate-700">
        <span className="material-icons align-middle">home</span>
      </button>

      {user ? (
          <button onClick={handleLogout} title="Logout" className="p-2 semi-rounded-full bg-slate-900 hover:bg-slate-700">
        <span className="material-icons align-middle">logout</span>
        </button>
        ) : (
          <button onClick={() => navigate('/sign-in')} title="Login" className="p-2 semi-rounded-full bg-slate-900 hover:bg-slate-700">
        <span className="material-icons align-middle">login</span>
        </button>
        )}

    </div>
  );
}
