import { useState } from "react";
import { analyzeResume } from "../services/api";

const ROLES = [
  "Software Development Engineer",
  "Frontend Developer",
  "Backend Developer",
  "Full Stack Developer",
  "Data Scientist",
  "Data Analyst",
  "Machine Learning Engineer",
  "DevOps Engineer",
  "Product Intern",
];

function ResumeUpload({ onResult }) {
  const [resume, setResume] = useState(null);
  const [role, setRole] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resume) {
      setError("Please upload your resume");
      onResult(null);
      return;
    }

    if (!role && !jobDescription) {
      setError("Select a role or provide a job description");
      onResult(null);
      return;
    }

    setLoading(true);
    setError("");

    const jdToSend = jobDescription || role;

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jdToSend);
    formData.append("role", role);

    try {
      const data = await analyzeResume(formData);
      if (data.error) {
        setError(data.error);
        onResult(null);
      } else if (data.analysis && data.download_url) {
        onResult({ ...data.analysis, download_url: data.download_url });
      } else {
        setError("No analysis result received. Please try again.");
        onResult(null);
      }
    } catch (err) {
      setError("Resume analysis failed. Try again.");
      onResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-blue-200 rounded-3xl shadow-2xl flex flex-col md:flex-row overflow-hidden w-full max-w-2xl mx-auto md:max-w-3xl lg:max-w-4xl">
      {/* Left side: Icon and heading */}
      <div className="hidden md:flex flex-col items-center justify-center bg-gradient-to-br from-blue-900 via-gray-900 to-amber-700 px-12 py-16 border-r border-blue-100 min-w-[320px] max-w-[340px]">
        <div className="bg-white rounded-full p-6 mb-8 shadow">
          <svg
            className="w-16 h-16 text-blue-700"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 48 48"
          >
            <rect
              x="8"
              y="8"
              width="32"
              height="32"
              rx="6"
              stroke="currentColor"
              strokeWidth="3"
              fill="none"
            />
            <path
              d="M16 20h16M16 28h10"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
            />
          </svg>
        </div>
        <h2 className="text-3xl font-extrabold text-white text-center mb-3 tracking-tight">
          Upload Resume
        </h2>
        <p className="text-amber-100 text-center text-lg leading-relaxed font-medium">
          Analyze your resume for ATS compatibility and get actionable feedback.
        </p>
      </div>
      {/* Right side: Form */}
      <div className="flex-1 px-6 sm:px-10 py-10 flex flex-col justify-center min-w-0">
        <form
          onSubmit={handleSubmit}
          className="space-y-10 w-full max-w-lg mx-auto"
        >
          {/* Resume */}
          <div>
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Resume{" "}
              <span className="text-blue-700 font-semibold">(PDF)</span>
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
              className="block w-full text-base border border-blue-200 rounded-xl px-5 py-4 bg-blue-50 text-blue-700 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border file:border-blue-300 file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200 transition"
            />
          </div>

          {/* Role */}
          <div>
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Target Role{" "}
              <span className="text-gray-400 font-normal">(optional)</span>
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full rounded-xl border border-blue-200 bg-white p-4 text-gray-900 focus:ring-2 focus:ring-blue-500 outline-none text-base"
            >
              <option value="">Select a role</option>
              {ROLES.map((r, i) => (
                <option key={i} value={r}>
                  {r}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-400 mt-2">
              Role helps infer missing job requirements
            </p>
          </div>

          {/* JD */}
          <div>
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Job Description{" "}
              <span className="text-gray-400 font-normal">(optional)</span>
            </label>
            <textarea
              rows="6"
              className="w-full rounded-xl border border-blue-200 bg-white p-5 text-gray-900 focus:ring-2 focus:ring-blue-500 outline-none text-base"
              placeholder="Paste the job description here for best accuracy"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          {/* Submit */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 rounded-2xl bg-blue-700 text-white font-bold hover:bg-amber-700 transition text-lg shadow-lg"
            >
              {loading ? (
                <span>
                  <svg
                    className="inline w-5 h-5 mr-2 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v8z"
                    ></path>
                  </svg>
                  Analyzing Resume...
                </span>
              ) : (
                "Run ATS Analysis"
              )}
            </button>
          </div>

          {error && (
            <div className="pt-2">
              <p className="text-red-600 text-base text-center">{error}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default ResumeUpload;
