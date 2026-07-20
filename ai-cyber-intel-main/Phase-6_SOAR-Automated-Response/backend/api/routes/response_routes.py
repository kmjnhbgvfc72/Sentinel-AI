from fastapi import APIRouter
from app.automation.response_executor import ResponseExecutor

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("/recommend")
def recommend(action: str):
    return ResponseExecutor().execute(action)
