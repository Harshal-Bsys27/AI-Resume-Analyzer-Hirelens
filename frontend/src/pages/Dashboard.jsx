import { useState } from "react";
import Navbar from "../components/Navbar";
import ResumeUpload from "../components/ResumeUpload";
import Scorecard from "../components/Scorecard";
import ScoreChart from "../components/ScoreChart";
import SkillsTags from "../components/SkillsTags";
import AnalysisResult from "../components/AnalysisResult";

// Demo data for initial dashboard view
const DEMO = {
  overall_score: 72,
  score_breakdown: {
    skills_match: 65,
    experience_match: 80,
    education_match: 70,
  },
  chart_data: {
    "Tech Stack Coverage": 60,
    "Skills Match": 65,
    "Experience Match": 80,
    "Education Match": 70,
    "Semantic Similarity": 55,
    "Overall ATS Score": 72,
  },
  skills: {
    matched_skills: ["python", "react", "sql"],
    missing_skills: ["docker", "aws"],
    extra_skills: ["c++"],
  },
};

function Dashboard() {
  const [result, setResult] = useState(null);

  // Use demo data if no result yet
  const scorecardData = result
    ? { overall: result.overall_score, breakdown: result.score_breakdown }
    : { overall: DEMO.overall_score, breakdown: DEMO.score_breakdown };

  // Build chart data from result if not present
  let chartData;
  if (result) {
    if (result.chart_data) {
      chartData = result.chart_data;
    } else {
      chartData = {
        "Tech Stack Coverage": result.techstack_coverage ?? 0,
        "Skills Match": result.score_breakdown?.skills_match ?? 0,
        "Experience Match": result.score_breakdown?.experience_match ?? 0,
        "Education Match": result.score_breakdown?.education_match ?? 0,
        "Semantic Similarity": result.semantic_score ?? 0,
        "Overall ATS Score": result.overall_score ?? 0,
      };
    }
  } else {
    chartData = DEMO.chart_data;
  }

  const skills = result ? result.skills : DEMO.skills;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 pb-16">
      <Navbar />
      <div className="max-w-7xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-extrabold mb-8 text-orange-700 flex items-center gap-3">
          <span className="w-12 h-12 rounded-xl bg-white flex items-center justify-center text-amber-700 font-extrabold text-2xl shadow-lg border-2 border-gray-900">HL</span>
          HireLens ATS Dashboard
        </h1>
        {/* ATS Analysis Summary Section */}
        <section className="bg-white/95 border border-orange-100 rounded-2xl shadow-xl p-8 mb-10">
          <h2 className="text-2xl md:text-3xl font-extrabold text-orange-700 mb-6 tracking-tight text-center">
            ATS Analysis Summary
          </h2>
          <div className="flex flex-col lg:flex-row gap-8 items-stretch">
            <div className="flex-1 flex flex-col gap-6 justify-between">
              <Scorecard overall={scorecardData.overall} breakdown={scorecardData.breakdown} />
              <div>
                <h3 className="text-lg font-semibold mb-2 text-orange-700">Skill Tags</h3>
                <SkillsTags skills={skills} />
              </div>
            </div>
            <div className="flex-1 flex items-center">
              <ScoreChart chartData={chartData} />
            </div>
          </div>
        </section>
        <div className="mt-10">
          <ResumeUpload onResult={setResult} />
        </div>
        {!result && (
          <div className="mt-10 text-center text-gray-500 text-lg">
            <p>
              Upload your resume and select a role or paste a job description to see your personalized ATS analysis here.
            </p>
            <p className="mt-2 text-sm text-gray-400">
              (Demo data is shown above until you upload your own resume.)
            </p>
          </div>
        )}
        {result && (
          <div className="mt-10">
            <AnalysisResult data={result} />
          </div>
        )}
      </div>
    </div>
  );
}
export default Dashboard;
