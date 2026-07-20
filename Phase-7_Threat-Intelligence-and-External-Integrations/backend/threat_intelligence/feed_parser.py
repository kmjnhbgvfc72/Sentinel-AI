import csv
import io
import json


class FeedParseError(ValueError):
    pass


class FeedParser:
    @staticmethod
    def parse(content: str, feed_format: str) -> list[dict]:
        try:
            if feed_format == "json":
                parsed = json.loads(content)
                rows = parsed.get("indicators", parsed.get("data", [])) if isinstance(parsed, dict) else parsed
            elif feed_format == "csv":
                rows = list(csv.DictReader(io.StringIO(content)))
            elif feed_format == "text":
                rows = [{"value": line.strip()} for line in content.splitlines() if line.strip() and not line.lstrip().startswith("#")]
            else:
                raise FeedParseError(f"Unsupported feed format: {feed_format}")
        except (json.JSONDecodeError, csv.Error, UnicodeError) as exc:
            raise FeedParseError("Feed content is malformed") from exc
        if not isinstance(rows, list):
            raise FeedParseError("Feed must contain a list of indicators")
        return [row if isinstance(row, dict) else {"value": str(row)} for row in rows]
