function AnalysisResult({ data }) {
  if (!data) return null;

  return (
    <div className="max-w-5xl mx-auto mt-10 px-6 text-slate-800">

      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 mb-6">
        <h2 className="text-3xl font-semibold mb-1">
          Resume Analysis Report
        </h2>
        <p className="text-slate-500">
          Detected Role:{" "}
          <span className="text-blue-600 font-medium capitalize">
            {data.role_detected}
          </span>
        </p>
      </div>

      {/* Score Cards */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-3">Overall ATS Score</h3>
          <div className="text-5xl font-bold text-blue-600">
            {data.overall_score}%
          </div>
          <p className="text-slate-500 mt-2">
            Based on skills, experience & education
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-4">Score Breakdown</h3>
          <ul className="space-y-2 text-slate-600">
            <li>Skills Match: <span className="font-medium">{data.score_breakdown.skills_match}%</span></li>
            <li>Experience Match: <span className="font-medium">{data.score_breakdown.experience_match}%</span></li>
            <li>Education Match: <span className="font-medium">{data.score_breakdown.education_match}%</span></li>
          </ul>
        </div>
      </div>

      {/* Skills */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-3 text-green-600">
            Matched Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {data.skills.matched_skills.length > 0 ? (
              data.skills.matched_skills.map((skill, i) => (
                <span
                  key={i}
                  className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-slate-500">No matched skills found</p>
            )}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-3 text-red-600">
            Missing Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {data.skills.missing_skills.length > 0 ? (
              data.skills.missing_skills.map((skill, i) => (
                <span
                  key={i}
                  className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-slate-500">No missing skills 🎉</p>
            )}
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-3">Strengths</h3>
          <ul className="list-disc list-inside text-slate-600 space-y-1">
            {data.strengths.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-3">Weaknesses</h3>
          <ul className="list-disc list-inside text-slate-600 space-y-1">
            {data.weaknesses.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Suggestions */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 mb-10">
        <h3 className="text-lg font-semibold mb-3 text-blue-600">
          Improvement Suggestions
        </h3>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          {data.suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {/* Download */}
      <div className="text-center mb-16">
        <button className="bg-blue-600 text-white font-medium px-6 py-3 rounded-lg hover:bg-blue-700 transition">
          Download Report (PDF)
        </button>
      </div>

    </div>
  );
}

export default AnalysisResult;
