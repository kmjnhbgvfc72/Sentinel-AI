import os
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_soc.db")
os.environ.setdefault("JWT_SECRET", "test-secret-that-is-long-enough-for-tests")
from ai_production.risk_scoring import RiskFactors, calculate_risk, risk_level
from security.authentication import create_access_token
from threat_response.executor import ResponseExecutor


def test_risk_score_and_level():
    score = calculate_risk(RiskFactors(1, 1, 1, 1))
    assert score == 100 and risk_level(score) == "critical"


def test_token_created():
    assert isinstance(create_access_token("analyst", ["analyst"]), str)


def test_response_target_validation():
    ResponseExecutor._validate("block_ip", "203.0.113.9")
    try: ResponseExecutor._validate("block_ip", "not-ip")
    except ValueError: pass
    else: raise AssertionError("invalid IP accepted")

