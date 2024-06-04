from typing import TYPE_CHECKING

from pytest import fixture

from shared.utils import reverse_url

if TYPE_CHECKING:
    from httpx import AsyncClient

    from shared.types import ASGIApp


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
    httpx_client: tuple["AsyncClient", "ASGIApp"], bill_data: tuple[dict, dict]
) -> list[dict]:
    client, app = httpx_client
    endpoint = reverse_url(application=app, controller_name="bills:create")
    return [(await client.post(endpoint, json=data)).json() for data in bill_data]
