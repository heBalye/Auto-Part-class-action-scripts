import codecs
import concurrent.futures
import glob
import json
import sys

import pandas as pd
import requests

# API URL
url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"

# Create chunk that contains 500 vins
Dict = {}
for i in range(len(vin_df["VIN"]) // 500 + 1):
    if (i + 1) * 500 < len(vin_df["VIN"]):
        Dict["Chunk" + str(i)] = ";".join(
            vin_df["VIN"][(i + 1) * 500 - 500 : (i + 1) * 500]
        )
    else:
        Dict["Chunk" + str(i)] = ";".join(vin_df["VIN"][(i + 1) * 500 - 500 :])
    print((i + 1) * 500 - 500, (i + 1) * 500)
# Chunk list 
Chunks = [Cunk for Chunk in Dict]
# MainBody

def getValid(chunk):
    post_fields = {"format": "json", "data": Dict[Chunk]}
    r = requests.post(url, data=post_fields)
    result = json.loads(r.text)
    df = pd.DataFrame(result["Results"])[
        [
            "VIN",
            "BodyClass",
            "Make",
            "Manufacturer",
            "Model",
            "ModelYear",
            "Series",
            "Trim",
            "VehicleType",
            "SuggestedVIN",
            "ErrorText",
        ]
    ]
    return df

with concurrent.fures.ThreadPoolExecutor() as exe:
    results = exe.map(getValid，Chunks)

concat = pd.concat([result for result in results])
