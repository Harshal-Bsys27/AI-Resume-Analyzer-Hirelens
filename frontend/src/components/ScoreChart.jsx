import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

function ScoreChart({ chartData }) {
  if (!chartData) return null;
  // Convert chartData object to array for recharts
  const data = Object.entries(chartData).map(([name, value]) => ({ name, value }));

  return (
    <div className="bg-white border rounded-2xl p-8 my-4 shadow-lg flex flex-col items-center min-h-[380px] w-full xl:w-[700px] mx-auto">
      <div className="font-bold text-xl mb-6 text-orange-700 tracking-tight">Score Chart</div>
      <ResponsiveContainer width="100%" minWidth={500} height={320}>
        <BarChart data={data} barSize={38} margin={{ top: 20, right: 40, left: 20, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" fontSize={15} tick={{ fill: '#b45309', fontWeight: 600 }} interval={0} angle={-12} textAnchor="end" height={70} />
          <YAxis domain={[0, 100]} tick={{ fill: '#334155', fontWeight: 600 }} />
          <Tooltip />
          <Bar dataKey="value" fill="#fb923c" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
export default ScoreChart;
