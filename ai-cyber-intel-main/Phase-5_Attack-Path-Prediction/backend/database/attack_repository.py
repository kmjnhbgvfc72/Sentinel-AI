from collections.abc import AsyncGenerator
import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config.attack_settings import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncGenerator[Session, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def initialize_database() -> None:
    from models import Asset, AttackGraphEdge, AttackPath, Recommendation, RiskScore  # noqa: F401

    Base.metadata.create_all(bind=engine)


class AttackRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_analysis(self, paths: list[dict], edges: list[dict], assets: list[dict], recommendations: list[dict]) -> None:
        from models import Asset, AttackGraphEdge, AttackPath, Recommendation

        for path in paths:
            self.session.add(AttackPath(source_node=path["path"][0], destination_node=path["path"][-1], path=json.dumps(path["path"]), risk_score=path["risk_score"], risk_level=path["risk_level"]))
        for edge in edges:
            self.session.add(AttackGraphEdge(**edge))
        for asset in assets:
            row = self.session.scalar(select(Asset).where(Asset.asset_name == asset["asset_name"]))
            if row:
                row.risk_score, row.criticality = asset["risk_score"], asset["criticality"]
            else:
                self.session.add(Asset(asset_name=asset["asset_name"], asset_type=asset["asset_type"], criticality=asset["criticality"], risk_score=asset["risk_score"]))
        for recommendation in recommendations:
            self.session.add(Recommendation(**recommendation))
        self.session.commit()

    def paths(self, limit: int) -> list:
        from models import AttackPath
        return list(self.session.scalars(select(AttackPath).order_by(AttackPath.created_at.desc()).limit(limit)))

    def graph(self) -> list:
        from models import AttackGraphEdge
        return list(self.session.scalars(select(AttackGraphEdge).order_by(AttackGraphEdge.created_at.desc()).limit(500)))

    def assets(self, limit: int) -> list:
        from models import Asset
        return list(self.session.scalars(select(Asset).order_by(Asset.risk_score.desc()).limit(limit)))

    def recommendations(self, limit: int) -> list:
        from models import Recommendation
        return list(self.session.scalars(select(Recommendation).order_by(Recommendation.created_at.desc()).limit(limit)))
