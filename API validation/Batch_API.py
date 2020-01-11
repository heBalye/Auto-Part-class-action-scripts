import codecs
import concurrent.futures
import glob
import json
import sys

import pandas as pd
import requests

# get target table

# vin_df = pd.read_excel(
#     "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\VIN API\\Source\\Rexel_01032020 vins.xlsx",
#     dtype=str,
# )
with open("./test/example.txt", "r") as text:
    VIN_string = text.read()

Vin_list = VIN_string.split(";")
# # API URL
# url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"

# Create chunk that contains 4 vins
Dict = {}
for i in range(len(Vin_list) // 4 + 1):
    if (i + 1) * 4 < len(Vin_list):
        Dict["Chunk" + str(i)] = ";".join(Vin_list[(i + 1) * 4 - 4 : (i + 1) * 4])
    else:
        Dict["Chunk" + str(i)] = ";".join(Vin_list[(i + 1) * 4 - 4 :])
    print((i + 1) * 4 - 4, (i + 1) * 4)
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
    print(f"{Chunk} is done!")
    return df


concat = pd.DataFrame()

with concurrent.futures.ThreadPoolExecutor() as exe:
    results = exe.map(getValid, Chunks[:25])
    for result in results:
        concat = pd.concat([concat, result])

print(concat)

# concat = pd.concat([result for result in results])

# print(concat)
