# SOC User Flows

## Dashboard navigation

The analyst enters the Security Overview, reviews the five headline indicators and risk explanation, then uses the sidebar without page reloads. Dashboard datasets refresh at the configured interval, display the last successful update, and pause polling while the tab is hidden.

## Threat investigation

1. Open **Threats**.
2. Search or filter by severity, status, category, and sort order; key filters are stored in the URL.
3. Select **View details** for evidence, affected assets, defensive recommendations, and the activity timeline.
4. Use this read-only Phase 2 context to guide the documented analyst process.

## Alert acknowledgement and resolution

1. Open **Alerts** and filter the queue.
2. Inspect alert source, asset, severity, and timestamps.
3. Choose **Acknowledge**, **Resolve**, or **Reopen investigation**.
4. Confirm the recorded status change.
5. Review success or error feedback. The backend rejects unsupported transitions and records valid transitions in its repository boundary.

## Asset inspection

Open **Assets**, filter by type, health, or risk, and select **Inspect**. The detail panel provides owner, platform, address, last-seen time, health, score, and open-alert count.

## Report generation

Open **Reports**, select a date range, and review posture, severity, resolution, trends, and affected assets. **Export threat CSV** downloads a real API-generated CSV. **Print / Save PDF** invokes the browser’s print workflow using a dedicated print layout.
