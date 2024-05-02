from src.epc_api import epc_api_call
from src.property import Property
from dotenv import load_dotenv
import os 
from src.utils import *
from tests.test_os_api import os_api_call
import json

with open("src/os_dummy_data.json") as data:
    os_dummy_data = json.load(data)

load_dotenv()

TOKEN = os.getenv('EPC_ENCODED_API_TOKEN')


BASE_URL = 'https://epc.opendatacommunities.org/api/v1/domestic/search?'
HEADERS = {
        'Accept': 'application/json',
        'Authorization': f'Basic {TOKEN}'
    }

OS_API_KEY = os.getenv("OS_API_KEY")
OS_PARAMS = {
        "key": OS_API_KEY,
        "limit": 2,
        "filter": "oslandusetiera LIKE 'Residential Accommodation' AND ismainbuilding=true",
        "bbox": "-0.372438,51.405655,-0.371885,51.40600",
    }




def test_returns_two_rows_of_properties():
    array_of_properties = epc_api_call(HEADERS, 'local-authority=E09000008&size=2')['rows']
    assert len(array_of_properties) == 2

def test_returns_multiple_buildings_from_os():
    response = os_api_call({"Accept":"application/json"}, OS_PARAMS)
    array_of_buildings = response["features"]
    assert len(array_of_buildings) > 1
    assert len(os_dummy_data["features"]) > 1
    
array_of_buildings = os_dummy_data["features"]
props = get_props_from_os(array_of_buildings)
def test_returns_array_of_property_instances_from_os():
    assert type(props) is list
    assert type(props[0]) is Property

def test_properties_have_desired_attributes():
    assert props[0].connectivity == "Semi-Connected"
    assert props[0].age == "1945-1959"
    assert props[0].material == "Brick Or Block Or Stone"
    assert props[0].uprn == 100061342030
    assert props[1].uprn == 100061342031
    assert props[2].connectivity == "Multi-Connected"
    assert props[2].uprn == 10033322698
    assert props[2].age == 2012
    assert props[2].material == "Brick Or Block Or Stone"
    assert props[0].epc_rating != ''
    assert props[0].epc_score != ''
    assert props[0].address != ''

# def get_urpns_from_properties(properties):
#     result = {}
#     for prop in properties:

#     return result

# def test_getting_uprns_from_os_dummy_date_for_epc_call():
#     assert type(get_urpns_from_properties(props)) is dict
#     assert len(get_urpns_from_properties(props)) > 0