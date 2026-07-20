import { render, screen } from "@testing-library/react";
import RiskScoreCard from "./RiskScoreCard";
test("renders bounded risk score", () => { render(<RiskScoreCard risk={{ risk_score: 92, severity: "critical" }}/>); expect(screen.getByText("92")).toBeInTheDocument(); expect(screen.getByText("critical")).toBeInTheDocument(); });
