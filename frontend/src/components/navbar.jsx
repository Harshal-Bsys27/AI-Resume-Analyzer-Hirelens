import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-gradient-to-r from-gray-900 via-gray-800 to-amber-700 border-b border-gray-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-white flex items-center justify-center text-amber-700 font-extrabold text-2xl shadow-lg border-2 border-gray-900">
            HL
          </div>
          <div>
            <p className="text-2xl font-bold text-white leading-none tracking-wide">
              HireLens Resume Analyzer
            </p>
            <p className="text-xs text-amber-200 font-medium">
              ATS Resume Analysis for Real Results
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-10 text-white font-medium">
          <a className="hover:text-amber-400 transition" href="#">
            Home
          </a>
          <a className="hover:text-amber-400 transition" href="#">
            Analyze
          </a>
          <a className="hover:text-amber-400 transition" href="#">
            Jobs
          </a>
          {/*  <Link className="hover:text-amber-400 transition" to="/dashboard">
            Dashboard
          </Link>*/}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-4">
          <button className="hidden sm:block text-white hover:text-amber-400 transition">
            Login
          </button>
          <Link
            to="/get-started"
            className="px-5 py-2 rounded-xl bg-white text-amber-700 font-semibold hover:bg-amber-100 transition shadow-lg border-2 border-gray-900"
          >
            Get Started
          </Link>
        </div>

      </div>
    </header>
  );
}

export default Navbar;
