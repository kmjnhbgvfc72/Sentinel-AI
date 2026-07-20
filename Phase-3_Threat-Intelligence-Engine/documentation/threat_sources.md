# Threat Sources

The CVE collector supports the NIST NVD CVE 2.0 API. Network collection requires `EXTERNAL_FEEDS_ENABLED=true`; the optional NVD key is read only from the environment. Deployments must respect provider rate limits and attribution terms.

IP, domain, and file-hash collectors normalize records supplied by an approved commercial, community, or internal reputation provider. Authentication, firewall, and application logs must come from already-authorized telemetry. Passwords, tokens, cookies, authorization values, secrets, API keys, and credential fields are removed before log persistence.

Demo records use documentation-reserved IP/domain ranges and synthetic hashes.
