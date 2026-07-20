import asyncio
from collections.abc import AsyncIterator
from ai_production.prediction_engine import PredictionEngine
from ai_production.risk_scoring import RiskFactors


async def inference_stream(events: AsyncIterator[dict], engine: PredictionEngine):
    async for event in events:
        factors = RiskFactors(*(float(event.get(key, 0)) for key in ("anomaly_score", "asset_criticality", "threat_confidence", "exposure")))
        yield {"event_id": event.get("id"), **await asyncio.to_thread(engine.predict, factors, event)}

