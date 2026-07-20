# SOC Dashboard Design

## Design system

The interface uses a dark-first, low-distraction system with an 8px spacing rhythm, compact operational typography, 6–10px corner radii, subtle one-pixel borders, and restrained transitions. Deep navy surfaces separate content without excessive shadows or glass effects. Cyan identifies navigation and interactive controls.

Severity is never conveyed by color alone. Every indicator includes a text label:

| Severity | Color | Meaning |
|---|---|---|
| Critical | Red `#ff5c6c` | Immediate analyst review |
| High | Orange `#ff9855` | Significant exposure |
| Medium | Amber `#f4c95d` | Review and prioritize |
| Low | Green `#42d392` | Low current exposure |

## Layout and reusable components

The application shell keeps navigation and context stable. The sidebar provides route state, collapse behavior, and an accessible mobile drawer. The navbar presents the page title, global search affordance, time range, platform health, notifications, and analyst identity. `ThreatCard`, `AlertCard`, `RiskScore`, `SeverityBadge`, `Modal`, `PageState`, and `Pagination` keep content and behavior consistent.

The line chart is used for change over time and keeps each severity visible with a legend and tooltip. The donut chart makes distribution proportions scannable while the API also returns explicit counts and percentages. Chart containers are responsive and include accessible descriptions.

## Responsive behavior

- Desktop: persistent sidebar, multi-column executive view, full data tables.
- Tablet: reduced navigation metadata and two-column visualizations.
- Mobile: drawer navigation, single-column cards, horizontally scrollable semantic tables, full-width controls, and side panels sized to the viewport.

## Accessibility

Semantic headings, tables, forms, navigation landmarks, ARIA labels, text severity labels, keyboard-accessible controls, visible focus rings, escape-to-close panels, adequate contrast, and `prefers-reduced-motion` support are included. Status changes require explicit confirmation and produce feedback.
