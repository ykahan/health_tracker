from __future__ import annotations

from typing import Iterator

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

ENGINE_URL = "sqlite:///health.db"
engine = create_engine(ENGINE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
