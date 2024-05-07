from flask import Flask, render_template
from src.os_api import os_api_call
from src.utils import get_props_from_os, get_attributes_from_epc
from src.variables import OS_KEY

app = Flask(__name__)

@app.route("/")
def home():
    list_of_buildings = os_api_call({"Accept":"application/json"}, {
        "key": OS_KEY,
        "filter": "oslandusetiera LIKE 'Residential Accommodation' AND ismainbuilding=true",
        "bbox": "-0.373641,51.399234,-0.372031,51.399977",
    })["features"]
    props = get_props_from_os(list_of_buildings)
    get_attributes_from_epc(props)
    for i in range(len(props)):
        props[i].calculate_score()
    return render_template("home.html", props=props)


# Define other routes as needed

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
