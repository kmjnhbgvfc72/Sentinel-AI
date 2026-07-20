import { render, screen } from "@testing-library/react";
import ThreatFeed from "./ThreatFeed";
test("renders normalized threat", () => { render(<ThreatFeed threats={[{ id: 1, name: "Observed threat", description: "Defensive record", severity: "high", risk_score: 80, source: "test", created_at: "2026-01-01T00:00:00Z" }]}/>); expect(screen.getByText("Observed threat")).toBeInTheDocument(); });
