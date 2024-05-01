import urllib.request
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
import json

load_dotenv()

with open("src/os_dummy_data.json", "r") as data:
    os_dummy_data = json.load(data)

HEADERS = {"Accept": "application/json"}
BASE_URL = "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-2/items?"
OS_API_KEY = os.getenv("OS_API_KEY")


def os_api_call(headers, params):
    full_url = f"{BASE_URL}{urlencode(params)}"
    try:
        with urllib.request.urlopen(
            urllib.request.Request(full_url, headers=headers)
        ) as response:
            response_body = response.read()
            return json.loads(response_body)

    except Exception:
        return False


response = os_api_call(
    HEADERS,
    {
        "key": OS_API_KEY,
        "limit": 3,
        "filter": "oslandusetiera LIKE 'Residential Accommodation' AND ismainbuilding=true",
        "bbox": "-0.372438,51.405655,-0.371885,51.40600",
    },
)
# https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-2/items?key=eQZohxBxjpHhrXsRrcVCxu5TI1XFObsw&filter=oslandusetiera%20LIKE%20'Residential Accommodation'%20AND%20ismainbuilding=true&bbox=-0.372438,51.405655,-0.371885,51.40600&limit=3


def test_not_200_response():
    assert os_api_call({}, {}) == False


def test_200_response():
    assert type(response) is dict


def test_features_array_is_populated():
    assert len(response["features"]) > 0


def test_accessing_desired_response_data():
    first_building = response["features"][0]["properties"]
    assert first_building["connectivity"] == "Semi-Connected"
    year = (
        first_building["buildingage_year"]
        if first_building["buildingage_year"]
        else first_building["buildingage_period"]
    )
    assert year == "1945-1959"

    for i in range(len(response["features"])):
        response_building = response["features"][i]["properties"]
        dummy_data_building = os_dummy_data["features"][i]["properties"]
        assert response_building["connectivity"] == dummy_data_building["connectivity"]
        for j in range(len(response_building["uprnreference"])):
            assert (
                response_building["uprnreference"][j]["uprn"]
                == dummy_data_building["uprnreference"][j]["uprn"]
            )
