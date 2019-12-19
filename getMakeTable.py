import json

import httplib2
import pandas as pd


def getMake():
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
    h = httplib2.Http()
    _, content = h.request(url, "GET")
    result = json.loads(content)
    return pd.DataFrame(result["Results"])
