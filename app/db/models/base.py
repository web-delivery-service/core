from sqlalchemy.orm import (
    DeclarativeBase,
    declarative_mixin,
    mapped_column,
    Mapped,
    declared_attr,
)
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import TypeVar


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


@declarative_mixin
class IDBaseModel:
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )


@declarative_mixin
class TimeStampedCreateModel:
    """
    An abstract base class model that provides create date information
    ``created_at``
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


@declarative_mixin
class TimeStampedUpdateModel:
    """
    An abstract base class model that provides update date information
    ``updated_at``
    """

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


ModelType = TypeVar("ModelType", bound=Base)
