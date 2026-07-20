"""Confidence calibration for explainable predictions."""


class ConfidenceScorer:
    def calculate(self, model_probability: float, data_quality: float, evidence_count: int) -> dict[str, object]:
        probability = min(1.0, max(0.0, model_probability))
        quality = min(1.0, max(0.0, data_quality))
        evidence = min(1.0, max(0, evidence_count) / 10)
        score = round(0.6 * probability + 0.25 * quality + 0.15 * evidence, 4)
        return {"confidence": score, "band": "high" if score >= 0.75 else "medium" if score >= 0.45 else "low", "components": {"model": probability, "data_quality": quality, "evidence": evidence}}
