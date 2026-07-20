"""Continuous-learning tests."""
from ai_learning.feedback_engine import FeedbackEngine
from ai_learning.self_learning import SelfLearningEngine


def test_learning_trains_scores_and_versions_model() -> None:
    engine = SelfLearningEngine()
    version = engine.learn([[0, 0], [0.1, 0.2], [0.2, 0.1], [9, 9]])
    result = engine.assess([8, 8])
    assert version.active
    assert 0 <= result["anomaly_score"] <= 1
    assert result["model_version"] == version.version_id


def test_feedback_quality_and_noisy_rules() -> None:
    feedback = FeedbackEngine()
    for index in range(3):
        feedback.record(str(index), "false_positive", "rule-1")
    assert feedback.quality()["precision"] == 0
    assert feedback.noisy_rules() == ["rule-1"]
