import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import AnalysisResult from "./components/AnalysisResult";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      {/* Navbar */}
      <nav className="bg-white shadow-sm px-6 py-4">
        <h1 className="text-xl font-bold text-gray-800">
          AI Resume Analyzer (ATS Simulator)
        </h1>
      </nav>

      {/* Main Dashboard */}
      <main className="max-w-6xl mx-auto px-6 py-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">
            Upload Resume
          </h2>
          <ResumeUpload onResult={setResult} />
        </section>

        {/* Result Section */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">
            ATS Analysis Result
          </h2>
          <AnalysisResult data={result} />
        </section>
      </main>
    </div>
  );
}

export default App;
