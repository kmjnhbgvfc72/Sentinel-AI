import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { titleCase } from "../utils";

const colors = { critical: "#ff5c6c", high: "#ff9855", medium: "#f4c95d", low: "#42d392" };
export default function RiskChart({ data = [] }) { return <div className="chart risk-chart" role="img" aria-label="Risk distribution by severity"><ResponsiveContainer width="100%" height={300}><PieChart><Pie data={data} dataKey="count" nameKey="severity" innerRadius={58} outerRadius={94} paddingAngle={3}>{data.map((item) => <Cell key={item.severity} fill={colors[item.severity]}/>)}</Pie><Tooltip formatter={(value, _name, context) => [`${value} (${context.payload.percentage}%)`, titleCase(context.payload.severity)]}/><Legend formatter={titleCase}/></PieChart></ResponsiveContainer></div>; }
