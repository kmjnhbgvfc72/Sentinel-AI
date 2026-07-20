import json
import logging
import re
from pathlib import Path
from collections.abc import Iterator

logger = logging.getLogger(__name__)
FAILED_LOGIN = re.compile(r"failed (?:password|login).*?(?:from|ip[=:])\s*([0-9a-fA-F:.]+)", re.I)


class LogCollector:
    def parse(self, line: str, source: str = "server") -> dict:
        try:
            data = json.loads(line)
            return {"source": source, "message": data.get("message", line), "raw": data}
        except json.JSONDecodeError:
            match = FAILED_LOGIN.search(line)
            return {"source": source, "message": line.strip(), "source_ip": match.group(1) if match else None, "suspicious": bool(match)}

    def tail(self, path: str) -> Iterator[dict]:
        resolved = Path(path).resolve(strict=True)
        with resolved.open(encoding="utf-8", errors="replace") as stream:
            for line in stream: yield self.parse(line)

