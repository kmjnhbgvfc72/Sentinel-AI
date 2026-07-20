# Previous Phase Integration

- Phase 3 log management supplies observables such as source/destination IP, domain, URL, and hash.
- Phase 4 AI detections receive corroborating IOC context and contribute risk/confidence to correlations.
- Phase 5 attack-path records gain threat-intelligence priority context for affected assets and predicted paths.
- Phase 6 SOAR incidents consume verified context for analyst decisions and defensive playbook selection.

Adapters are read-only and use short timeouts. No automatic containment or destructive action is triggered by Phase 7. Upstream failures degrade to stored correlations and local reputation. Exact endpoint shapes can be adapted in `IntegrationService` without coupling domain engines to prior codebases.
