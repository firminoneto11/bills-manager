from pytest import fixture


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
        "total": 3.0,
        "sub_bills": [
            {"id": 1, "amount": 1.0, "reference": "REF-1"},
            {"id": 2, "amount": 2.0, "reference": "ref-2"},
        ],
    }, {
        "id": 2,
        "total": 1.0,
        "sub_bills": [{"id": 3, "amount": 1.0, "reference": "INV-1"}],
    }


@fixture
def bill_data_failure_case():
    return {
        "total": 2,
        "sub_bills": [{"amount": 1, "reference": "INV-1"}],
    }
