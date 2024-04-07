from typing import TYPE_CHECKING

from pytest import fixture

from shared.utils import reverse_url

if TYPE_CHECKING:
    from fastapi import FastAPI
    from httpx import AsyncClient


app_name = "core:bills"


@fixture
def bill_data():
    return {
        "total": 3,
        "sub_bills": [
            {"amount": 1, "reference": "REF-1"},
            {"amount": 2, "reference": "ref-2"},
        ],
    }, {
        "total": 1,
        "sub_bills": [{"amount": 1, "reference": "INV-1"}],
    }


@fixture
def bill_data_expected_creation():
    return {
        "id": 1,
        "total": 3,
        "sub_bills": [
            {"amount": 1, "reference": "REF-1"},
            {"amount": 2, "reference": "ref-2"},
        ],
    }, {
        "id": 2,
        "total": 1,
        "sub_bills": [{"amount": 1, "reference": "INV-1"}],
    }


@fixture
def bill_data_failure_case():
    return {
        "total": 2,
        "sub_bills": [{"amount": 1, "reference": "INV-1"}],
    }


@fixture
async def setup_bill_data(
    asgi_app: "FastAPI", client: "AsyncClient", bill_data: tuple[dict, dict]
) -> list[dict]:
    endpoint = reverse_url(asgi_app, f"{app_name}:create")
    return [(await client.post(endpoint, json=data)).json() for data in bill_data]
