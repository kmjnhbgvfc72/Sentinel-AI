import { render, screen } from "@testing-library/react";
import AssetRiskCard from "./AssetRiskCard";
test("renders asset risk", () => { render(<AssetRiskCard asset={{ asset_name: "Database Server", asset_type: "database", criticality: 95, risk_score: 92 }}/>); expect(screen.getByText("Database Server")).toBeInTheDocument(); expect(screen.getByText("92")).toBeInTheDocument(); });
