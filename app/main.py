from uuid import UUID

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .database import get_db
from .schemas import WalletOperation, WalletResponse

app = FastAPI(title="Wallet API")


@app.post(
    "/api/v1/wallets/{wallet_uuid}/operation", response_model=WalletResponse
)
async def wallet_operation(
    wallet_uuid: UUID,
    operation: WalletOperation,
    db: AsyncSession = Depends(get_db),
):
    return await crud.handle_walelt_operation(
        db, wallet_uuid, operation.operation_type, operation.amount
    )


@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet(wallet_uuid: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.get_wallet_balance(db, wallet_uuid)


@app.post("/api/v1/wallets", response_model=WalletResponse)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    from .models import Wallet

    new_wallet = Wallet(balance=0)
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    return new_wallet


@app.get("/")
async def root():
    return {
        "Welcome to Wallet API. Go to /docs for API documentation."
    }
