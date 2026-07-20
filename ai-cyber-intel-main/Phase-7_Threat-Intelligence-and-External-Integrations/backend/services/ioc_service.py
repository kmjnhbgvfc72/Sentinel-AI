from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.errors import NotFoundError, ServiceError
from app.schemas import IOCInput
from database.repository import ThreatIntelligenceRepository
from threat_intelligence.validation import IOCValidationError, normalize_ioc


class IOCService:
    def __init__(self, repository: ThreatIntelligenceRepository):
        self.repository = repository

    def list(self, ioc_type: str | None, active: bool | None, limit: int):
        return self.repository.list_iocs(ioc_type=ioc_type, active=active, limit=limit)

    def create(self, payload: IOCInput):
        try:
            normalized = normalize_ioc(payload.type, payload.value)
        except IOCValidationError as exc:
            raise ServiceError(str(exc), code="invalid_ioc", status_code=422) from exc
        values = payload.model_dump()
        values["normalized_value"] = normalized
        values["tags"] = sorted({tag.strip().lower() for tag in payload.tags if tag.strip()})
        values["last_seen"] = datetime.now(UTC)
        try:
            item, created = self.repository.upsert_ioc(**values)
            self.repository.add_history(action="ioc_created" if created else "ioc_refreshed", entity_type="ioc", entity_id=str(item.id), details={"type": item.type, "source": item.source})
            self.repository.session.commit()
            self.repository.session.refresh(item)
            return item, created
        except IntegrityError as exc:
            self.repository.session.rollback()
            raise ServiceError("IOC already exists", code="duplicate_ioc", status_code=409) from exc

    def delete(self, ioc_id: int) -> None:
        item = self.repository.get_ioc(ioc_id)
        if not item:
            raise NotFoundError("IOC not found")
        self.repository.add_history(action="ioc_deleted", entity_type="ioc", entity_id=str(item.id), details={"type": item.type})
        self.repository.delete_ioc(item)
        self.repository.session.commit()
