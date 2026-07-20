"""Safe YARA wrapper with an explicit optional dependency."""
from pathlib import Path


class YaraScanner:
    def __init__(self) -> None:
        try:
            import yara
            self._yara = yara
        except ImportError:
            self._yara = None

    @property
    def available(self) -> bool:
        return self._yara is not None

    def scan_bytes(self, content: bytes, rule_source: str) -> list[dict[str, object]]:
        if len(content) > 10 * 1024 * 1024:
            raise ValueError("scan payload exceeds 10 MiB")
        if not self._yara:
            raise RuntimeError("yara-python is not installed")
        rules = self._yara.compile(source=rule_source)
        return [{"rule": match.rule, "namespace": match.namespace, "tags": list(match.tags)} for match in rules.match(data=content, timeout=10)]

    def scan_file(self, path: Path, rule_source: str) -> list[dict[str, object]]:
        return self.scan_bytes(path.read_bytes(), rule_source)
