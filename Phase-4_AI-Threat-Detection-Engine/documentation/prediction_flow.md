# Prediction Flow

Validated Phase 3 data → credential-safe processing → numeric features → anomaly detector and threat classifier → behavior flags → risk predictor → bounded score/severity → prediction and risk persistence → threshold-based alert → Phase 2 SOC dashboard.

The classifier returns Suspicious Login, Malware Indicator, Bot Activity, Data Access Anomaly, or Unknown Threat. Behavior flags explain device, location, time, frequency, IP, and authentication deviations. Alerts are generated when the final bounded risk meets `ALERT_RISK_THRESHOLD`.

Set `AUTO_ANALYZE_PHASE3=true` to pull the latest Phase 3 threats and sanitized logs once during Phase 4 startup. It is disabled by default so local startup does not depend on another service. Phase 3 API failures are intentionally visible during explicit integration startup rather than silently replaced with fabricated data.
