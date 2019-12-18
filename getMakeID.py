import json

import httplib2
import pandas as pd


def getMakeID(Make):
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
    h = httplib2.Http()
    _, content = h.request(url, "GET")
    result = json.loads(content)
    MK_df = pd.DataFrame(result["Results"])
    result_df = MK_df[MK_df["Make_Name"].str.contains(Make)]
    return result_df
