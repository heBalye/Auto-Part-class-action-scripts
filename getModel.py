import json

import httplib2
import pandas as pd


def getModel(Make):
    url = (
        "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/%s?format=json" % Make
    )
    h = httplib2.Http()
    _, content = h.request(url, "GET")
    result = json.loads(content)
    return pd.DataFrame(result["Results"])
