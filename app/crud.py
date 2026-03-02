from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Wallet


async def get_wallet_balance(db: AsyncSession, wallet_uuid: UUID):
    result = await db.execute(select(Wallet).where(Wallet.id == wallet_uuid))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(
            status_code=404, detail="Кошелёк не найден (Wallet not found)"
        )
    return wallet


async def handle_walelt_operation(
    db: AsyncSession, wallet_uuid: UUID, operation_type: str, amount: Decimal
):
    """Используем with_for_update() для блокировки строки в БД"""
    query = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()

    result = await db.execute(query)
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise HTTPException(
            status_code=404, detail="Кошелёк не найден (Wallet not found)"
        )

    if operation_type == "DEPOSIT":
        wallet.balance += amount
    elif operation_type == "WITHDRAW":
        if wallet.balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Недостаточно средств (Insufficient funds)",
            )
        wallet.balance -= amount

    await db.commit()
    await db.refresh(wallet)
    return wallet
