from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.attack_repository import Base


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_name: Mapped[str] = mapped_column(String(160), unique=True)
    asset_type: Mapped[str] = mapped_column(String(80))
    criticality: Mapped[int] = mapped_column(Integer)
    risk_score: Mapped[float] = mapped_column(Float)
