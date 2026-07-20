from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from database.attack_repository import Base


class AttackPath(Base):
    __tablename__ = "attack_paths"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_node: Mapped[str] = mapped_column(String(160))
    destination_node: Mapped[str] = mapped_column(String(160))
    path: Mapped[str] = mapped_column(String(2000))
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class AttackGraphEdge(Base):
    __tablename__ = "attack_graph"
    id: Mapped[int] = mapped_column(primary_key=True)
    node_type: Mapped[str] = mapped_column(String(50))
    node_value: Mapped[str] = mapped_column(String(160))
    relationship: Mapped[str] = mapped_column(String(100))
    target_node: Mapped[str] = mapped_column(String(160))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
