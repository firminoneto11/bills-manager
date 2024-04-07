from typing import TYPE_CHECKING

from sqlalchemy import func, select

from apps.core.models import Bills, SubBills
from shared.utils import reverse_url

if TYPE_CHECKING:
    from fastapi import FastAPI
    from httpx import AsyncClient
    from sqlalchemy.ext.asyncio import AsyncSession


app_name = "core:bills"


async def test_post_request_should_create_bills(
    asgi_app: "FastAPI",
    client: "AsyncClient",
    bill_data: tuple[dict, dict],
    bill_data_expected_creation: tuple[dict, dict],
):
    endpoint = reverse_url(asgi_app, f"{app_name}:create")

    response1, response2 = (
        await client.post(endpoint, json=bill_data[0]),
        await client.post(endpoint, json=bill_data[1]),
    )

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response1.json() == bill_data_expected_creation[0]
    assert response2.json() == bill_data_expected_creation[1]


async def test_creating_bill_with_wrong_amount_should_not_succeed(
    asgi_app: "FastAPI",
    client: "AsyncClient",
    bill_data_failure_case: dict,
    db_session: "AsyncSession",
):
    endpoint = reverse_url(asgi_app, f"{app_name}:create")

    response = await client.post(endpoint, json=bill_data_failure_case)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The bill's amount doesn't match the sum of its sub bills"
    }
    assert not (await db_session.scalar(select(func.count()).select_from(Bills)))
    assert not (await db_session.scalar(select(func.count()).select_from(SubBills)))
