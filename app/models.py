import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(
        Numeric(precision=12, scale=2), nullable=False, default=0.0
    )
