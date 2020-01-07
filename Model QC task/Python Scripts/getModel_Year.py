import json

import httplib2
import pandas as pd


def getModel_Year(Make, Year):
    url = (
        "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/%s/modelyear/%s?format=json"
        % (Make, Year)
    )
    h = httplib2.Http()
    _, content = h.request(url, "GET")
    result = json.loads(content)
    return pd.DataFrame(result["Results"])

