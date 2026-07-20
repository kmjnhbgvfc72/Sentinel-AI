import pytest

from threat_intelligence.feed_parser import FeedParseError, FeedParser
from threat_intelligence.scoring import ThreatScoreCalculator
from threat_intelligence.validation import IOCValidationError, normalize_ioc


def test_ioc_normalization():
    assert normalize_ioc("domain", "Example.COM.") == "example.com"
    assert normalize_ioc("url", "HTTPS://Example.COM/path#fragment") == "https://example.com/path"
    with pytest.raises(IOCValidationError):
        normalize_ioc("ip", "127.0.0.999")


def test_feed_parser_formats():
    assert FeedParser.parse('{"indicators":[{"type":"ip","value":"192.0.2.1"}]}', "json")[0]["type"] == "ip"
    assert len(FeedParser.parse("type,value\nip,192.0.2.1\n", "csv")) == 1
    with pytest.raises(FeedParseError):
        FeedParser.parse("{}", "xml")


def test_threat_score_is_bounded():
    calculator = ThreatScoreCalculator()
    assert calculator.calculate(confidence=100, severity="critical", reliability=100, sightings=100) == 100
    assert calculator.verdict(80) == "malicious"
