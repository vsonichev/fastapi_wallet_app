from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class WalletOperation(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class WalletResponse(BaseModel):
    id: UUID
    balance: Decimal

    class Config:
        from_attributes = True
