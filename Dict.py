import json

import httplib2
import pandas as pd

from Eiligble_table import ME_df


url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
h = httplib2.Http()
_, content = h.request(url, "GET")
result = json.loads(content)
ALL = pd.DataFrame(result["Results"])

Dict_temp = {}
for make in ME_df.Make.unique():
    try:
        a = ALL[ALL["Make_Name"].str.strip().str.lower() == make.lower()]
    except:
        Dict_temp[f"No ID for {make}"] = make.lower()
    else:
        Dict_temp[
            a.Make_ID.values[0] if len(a.Make_ID) > 0 else f"No ID for {make}"
        ] = make.lower()

Dict = Dict_temp

