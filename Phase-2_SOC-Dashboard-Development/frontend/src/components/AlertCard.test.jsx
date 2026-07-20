import { fireEvent, render, screen } from "@testing-library/react";
import AlertCard from "./AlertCard";
import SeverityBadge from "./SeverityBadge";

const alert = { id: 1, title: "Defensive test alert", severity: "critical", source: "Test sensor", asset: "test-asset", created_at: "2026-01-01T00:00:00Z", status: "new" };
test("renders accessible severity", () => { render(<SeverityBadge severity="critical"/>); expect(screen.getByLabelText("Severity: Critical")).toBeInTheDocument(); });
test("invokes alert status action", () => { const action = vi.fn(); render(<AlertCard alert={alert} onStatusChange={action}/>); fireEvent.click(screen.getByText("Acknowledge")); expect(action).toHaveBeenCalledWith(alert, "acknowledged"); });
