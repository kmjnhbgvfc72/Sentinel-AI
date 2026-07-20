import { fireEvent, render, screen } from "@testing-library/react";
import { ErrorState } from "./PageState";

test("renders API error and retry action", () => { const retry = vi.fn(); render(<ErrorState error={new Error("Service unavailable")} retry={retry}/>); expect(screen.getByRole("alert")).toHaveTextContent("Service unavailable"); fireEvent.click(screen.getByText("Retry")); expect(retry).toHaveBeenCalledOnce(); });
