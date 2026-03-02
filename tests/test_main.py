import asyncio
from uuid import uuid4

import httpx
import pytest

BASE_URL = "http://localhost:8000/api/v1/wallets"


@pytest.mark.asyncio
async def test_wallet_lifecycle():
    wallet_id = str(uuid4())

    async with httpx.AsyncClient() as client:
        """Проверка: кошелёк не найден"""
        resp = await client.get(f"{BASE_URL}/{wallet_id}")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_concurrent_withdraw():
    """Тестируем конуррентность. Снимаем деньги одновременно"""
    wallet_id = "e8162495-9bb5-4ca3-8cd8-236788b3d294"

    async with httpx.AsyncClient() as client:
        # Пополнени на 1000
        await client.post(
            f"{BASE_URL}/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 1000},
        )

        # Снимаем по 100, 10 раз одновременно
        tasks = []
        for _ in range(10):
            tasks.append(
                client.post(
                    f"{BASE_URL}/{wallet_id}/operation",
                    json={"operation_type": "WITHDRAW", "amount": 100},
                )
            )
        response = await asyncio.gather(*tasks)

        for r in response:
            assert r.status_code == 200

        # Проверка баланса, д.б. нулевой
        final_resp = await client.get(f"{BASE_URL}/{wallet_id}")
        assert float(final_resp.json()["balance"]) == 0
