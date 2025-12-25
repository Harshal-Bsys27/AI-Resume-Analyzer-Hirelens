import { useState } from "react";
import Navbar from "./components/navbar";
import ResumeUpload from "./components/ResumeUpload";
import AnalysisResult from "./components/AnalysisResult";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Navbar />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h1 className="text-5xl font-bold text-gray-900 leading-tight">
            AI-Powered <span className="text-blue-600">ATS Resume</span> Analyzer
          </h1>

          <p className="mt-6 text-lg text-gray-600">
            Simulate how real Applicant Tracking Systems scan, filter and score
            your resume. Improve your chances before you apply.
          </p>

          <div className="mt-8 flex gap-4">
            <button className="px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition">
              Analyze Resume
            </button>
            <button className="px-6 py-3 rounded-xl border border-gray-300 text-gray-700 hover:bg-gray-100 transition">
              Learn How ATS Works
            </button>
          </div>
        </div>

        {/* Upload Card */}
        <ResumeUpload onResult={setResult} />
      </section>

      {/* Result Section */}
      <section className="max-w-7xl mx-auto px-6 pb-16">
        <AnalysisResult data={result} />
      </section>
    </div>
  );
}

export default App;
