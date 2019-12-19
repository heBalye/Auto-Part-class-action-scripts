import json

import httplib2
import pandas as pd


def getOptions(MakeID, Year):
    url = (
        "https://vpic.nhtsa.dot.gov/api//vehicles/GetModelsForMakeIdYear/makeId/%s/modelyear/%s?format=json"
        % (MakeID, Year)
    )
    h = httplib2.Http()

    _, content = h.request(url, "GET")

    result = json.loads(content)

    return [item["Model_Name"] for item in result["Results"]]

