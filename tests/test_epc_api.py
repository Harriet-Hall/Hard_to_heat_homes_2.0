import os
from dotenv import load_dotenv
from src.epc_dummy_data import epc_dummy_data
from src.epc_api import epc_api_call

load_dotenv()

TOKEN = os.getenv("EPC_ENCODED_API_TOKEN")

QUERY_PARAMS = {"uprn": "200002791"}
BASE_URL = "https://epc.opendatacommunities.org/api/v1/domestic/search?"
HEADERS = {"Accept": "application/json", "Authorization": f"Basic {TOKEN}"}


def test_200_response():
    assert type(epc_api_call(HEADERS, QUERY_PARAMS)) is dict


def test_200_response_invalid_uprn():
    assert epc_api_call(HEADERS, {"uprn": "123456789"}) == {}


def test_not_200_response():
    assert epc_api_call({}, QUERY_PARAMS) == False


def test_result_is_JSON():
    assert epc_api_call(HEADERS, QUERY_PARAMS) == epc_dummy_data


def test_dummy_data_address():
    response_data = epc_api_call(HEADERS, QUERY_PARAMS)
    assert response_data["rows"][0]["address"] == epc_dummy_data["rows"][0]["address"]
    assert response_data["rows"][0]["address"] == "30 Alexandra Road, Muswell Hill"


def test_dummy_data_epc_rating():
    response_data = epc_api_call(HEADERS, QUERY_PARAMS)
    assert (
        response_data["rows"][0]["current-energy-rating"]
        == epc_dummy_data["rows"][0]["current-energy-rating"]
    )
    assert response_data["rows"][0]["current-energy-rating"] == "D"


def test_dummy_data_epc_score():
    response_data = epc_api_call(HEADERS, QUERY_PARAMS)
    assert (
        response_data["rows"][0]["current-energy-efficiency"]
        == epc_dummy_data["rows"][0]["current-energy-efficiency"]
    )
    assert response_data["rows"][0]["current-energy-efficiency"] == "63"