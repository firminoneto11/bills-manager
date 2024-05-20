from typing import TYPE_CHECKING

from pytest import mark
from sqlalchemy import func, select

from apps.bills.models import Bills, SubBills
from shared.utils import reverse_url

if TYPE_CHECKING:
    from fastapi import FastAPI
    from httpx import AsyncClient
    from sqlalchemy.ext.asyncio import AsyncSession


app_name = "bills"


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


async def test_get_request_should_return_empty_when_theres_no_data(
    asgi_app: "FastAPI", client: "AsyncClient"
):
    response = await client.get(reverse_url(asgi_app, f"{app_name}:list"))

    assert response.status_code == 200
    assert response.json() == []


async def test_get_request_should_return_data(
    asgi_app: "FastAPI", client: "AsyncClient", setup_bill_data: list[dict]
):
    response = await client.get(reverse_url(asgi_app, f"{app_name}:list"))

    assert response.status_code == 200
    assert response.json() == setup_bill_data


@mark.parametrize(
    argnames="query,expected_return",
    argvalues=[
        (
            "reference=ref-1",
            [{"id": 1, "total": 3, "sub_bills": [{"amount": 1, "reference": "REF-1"}]}],
        ),
        (
            "reference=ref",
            [
                {
                    "id": 1,
                    "total": 3,
                    "sub_bills": [
                        {"amount": 1, "reference": "REF-1"},
                        {"amount": 2, "reference": "ref-2"},
                    ],
                }
            ],
        ),
        (
            "reference=in",
            [
                {
                    "id": 2,
                    "total": 1,
                    "sub_bills": [{"amount": 1, "reference": "INV-1"}],
                }
            ],
        ),
        (
            "total_from=3",
            [
                {
                    "id": 1,
                    "total": 3,
                    "sub_bills": [
                        {"amount": 1, "reference": "REF-1"},
                        {"amount": 2, "reference": "ref-2"},
                    ],
                }
            ],
        ),
        (
            "total_to=2",
            [
                {
                    "id": 1,
                    "total": 3,
                    "sub_bills": [
                        {"amount": 2, "reference": "ref-2"},
                    ],
                }
            ],
        ),
    ],
)
async def test_get_request_with_parameters(
    asgi_app: "FastAPI",
    client: "AsyncClient",
    query: str,
    expected_return: list[dict],
    setup_bill_data: list[dict],
):
    response = await client.get(reverse_url(asgi_app, f"{app_name}:list") + f"?{query}")

    assert response.status_code == 200
    assert response.json() == expected_return
