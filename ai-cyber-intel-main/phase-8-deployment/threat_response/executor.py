import ipaddress
import logging
import re
from dataclasses import dataclass
from sqlalchemy.orm import Session
from config import get_settings
from database.models import ResponseAudit

logger = logging.getLogger(__name__)
DEVICE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
ACCOUNT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._@-]{0,127}$")


@dataclass(frozen=True)
class ResponseResult:
    action: str
    target: str
    status: str
    live_mode: bool
    message: str


class ResponseExecutor:
    """Policy-gated adapter. Wire provider callbacks to firewall, EDR and IdP APIs."""
    def __init__(self, providers: dict | None = None): self.providers = providers or {}

    def execute(self, db: Session, action: str, target: str, actor: str, approved: bool) -> ResponseResult:
        self._validate(action, target)
        live = get_settings().auto_response_enabled and approved
        if live:
            provider = self.providers.get(action)
            if not provider: raise RuntimeError(f"No live provider configured for {action}")
            provider(target)
            status, message = "completed", "Provider confirmed defensive action"
        else:
            status, message = "simulated", "Dry-run recorded; enable policy and approve request for live execution"
        result = ResponseResult(action, target, status, live, message)
        db.add(ResponseAudit(action=action, target=target, actor=actor, success=True, live_mode=live, result=result.__dict__))
        db.commit()
        logger.warning("response_action action=%s target=%s actor=%s live=%s", action, target, actor, live)
        return result

    @staticmethod
    def _validate(action: str, target: str):
        validators = {"block_ip": lambda v: ipaddress.ip_address(v), "isolate_device": lambda v: DEVICE_RE.fullmatch(v), "disable_account": lambda v: ACCOUNT_RE.fullmatch(v)}
        if action not in validators: raise ValueError("Unsupported response action")
        try: valid = validators[action](target)
        except ValueError as exc: raise ValueError("Invalid response target") from exc
        if not valid: raise ValueError("Invalid response target")

