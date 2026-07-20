from threat_intelligence.validation import IOCValidationError, normalize_ioc


class IOCMatchingEngine:
    """Exact normalized matching avoids unsafe fuzzy IOC attribution."""

    def match(self, iocs, event: dict) -> list:
        candidates: set[str] = set()
        for key in ("source_ip", "destination_ip", "ip", "domain", "url", "hash", "indicator"):
            value = event.get(key)
            if value:
                candidates.add(str(value).strip().lower())
        matches = []
        for ioc in iocs:
            try:
                normalized_candidates = {normalize_ioc(ioc.type, candidate) for candidate in candidates}
            except IOCValidationError:
                normalized_candidates = set()
                for candidate in candidates:
                    try:
                        normalized_candidates.add(normalize_ioc(ioc.type, candidate))
                    except IOCValidationError:
                        continue
            if ioc.normalized_value in normalized_candidates:
                matches.append(ioc)
        return matches
