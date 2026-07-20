import { render, screen } from "@testing-library/react";
import RiskScore from "./RiskScore";

test("renders risk score and label", () => { render(<RiskScore score={72} label="High" trend={-4}/>); expect(screen.getByLabelText(/72 out of 100/i)).toBeInTheDocument(); expect(screen.getByText("High")).toBeInTheDocument(); });
test("renders loading state", () => { render(<RiskScore loading/>); expect(screen.getByText(/loading risk score/i)).toBeInTheDocument(); });
test("renders empty state", () => { render(<RiskScore score={null}/>); expect(screen.getByText(/not available/i)).toBeInTheDocument(); });
