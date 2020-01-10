import codecs
import concurrent.futures
import glob
import json
import sys

import pandas as pd
import requests

# get target table

vin_df = pd.read_excel(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\VIN API\\Source\\Rexel_01032020 vins.xlsx",
    dtype=str,
)

# API URL
url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"

# Create chunk that contains 10 vins
Dict = {}
for i in range(len(vin_df["VIN"]) // 10 + 1):
    if (i + 1) * 10 < len(vin_df["VIN"]):
        Dict["Chunk" + str(i)] = ";".join(
            vin_df["VIN"][(i + 1) * 10 - 10 : (i + 1) * 10]
        )
    else:
        Dict["Chunk" + str(i)] = ";".join(vin_df["VIN"][(i + 1) * 10 - 10 :])
    print((i + 1) * 10 - 10, (i + 1) * 10)
# Chunk list
Chunks = [Chunk for Chunk in Dict]

# MainBody


def getValid(Chunk):
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"
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


# with concurrent.futures.ThreadPoolExecutor() as exe:
#     results = exe.map(getValid, Chunks)

# concat = pd.concat([result for result in results])
