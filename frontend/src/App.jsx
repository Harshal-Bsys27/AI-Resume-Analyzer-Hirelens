import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import ResumeUpload from "./components/ResumeUpload";
import AnalysisResult from "./components/AnalysisResult";
import HowAtsWorks from "./pages/HowATSWorks";
import GetStarted from "./pages/GetStarted";
import Dashboard from "./pages/Dashboard";

function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Navbar />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h1 className="text-5xl font-bold text-gray-900 leading-tight">
            AI-Powered <span className="text-purple-600">ATS Resume</span> Analyzer
          </h1>

          <p className="mt-6 text-lg text-gray-600">
            Simulate how real Applicant Tracking Systems scan, filter and score
            your resume. Improve your chances before you apply.
          </p>

          <div className="mt-8 flex gap-4 flex-wrap">
            <button className="px-6 py-3 rounded-xl bg-purple-600 text-white font-semibold hover:bg-blue-700 transition">
              Analyze Resume
            </button>
            <Link
              to="/how-ats-works"
              className="px-6 py-3 rounded-xl border border-purple-600 text-blue-700 hover:bg-blue-50 transition font-semibold"
            >
              Learn How ATS Works
            </Link>
            <Link
              to="/dashboard"
              className="px-6 py-3 rounded-xl border border-orange-500 text-orange-700 hover:bg-orange-50 transition font-semibold"
            >
              Dashboard
            </Link>
          </div>
        </div>

        {/* Upload Card */}
        <ResumeUpload onResult={setResult} />
      </section>

      {/* Result Section */}
      {result && (
        <section className="max-w-7xl mx-auto px-6 pb-16">
          <AnalysisResult data={result} />
        </section>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/how-ats-works" element={<HowAtsWorks />} />
        <Route path="/get-started" element={<GetStarted />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
