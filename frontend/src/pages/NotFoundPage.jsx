import { Link } from "react-router-dom";
import logo from "../ChatGPT.png";

export default function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-4">
      <img src={logo} alt="PahadSuraksha logo" className="h-16 w-16 rounded object-cover mb-4" />
      <h1 className="text-3xl font-display font-bold text-slate-50 mb-2">Lost on the trail</h1>
      <p className="text-slate-400 mb-6">This page doesn't exist.</p>
      <Link to="/" className="btn-primary">
        Back to home
      </Link>
    </div>
  );
}
