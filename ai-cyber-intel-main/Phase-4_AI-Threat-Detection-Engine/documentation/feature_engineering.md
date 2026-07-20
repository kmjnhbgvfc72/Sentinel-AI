# Feature Engineering

The processor derives a stable numeric vector containing failed-login count, IOC reputation, CVSS-like vulnerability score, activity-to-history frequency ratio, unknown-IP/new-device/location-change/abnormal-time/malware flags, severity encoding, and normalized data-access volume.

All values are bounded by Pydantic before processing. Historical averages use a minimum denominator to prevent division by zero. Credentials and authentication secrets are rejected from metadata and are never features. The feature order is recorded with model metadata to prevent training-serving skew.
