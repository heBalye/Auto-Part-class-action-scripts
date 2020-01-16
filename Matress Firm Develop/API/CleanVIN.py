import codecs
import concurrent.futures
import glob
import json
import sys

import pandas as pd
import requests

# # API URL
# url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"


def Col_to_str(df, col_name, separator):
    return separator.join(list(df[col_name]))


class ValidationProcess:
    def __init__(self, data, chunksize):
        self.data = data.split(";")
        self.chunksize = chunksize

    # Create chunk that contains vins in size of chunksize
    def split_to_Chunk(self, chunksize):
        Dict = {}
        for i in range(len(self.data) // chunksize + 1):
            if (i + 1) * chunksize < len(self.data):
                Dict["Chunk" + str(i)] = ";".join(
                    self.data[(i + 1) * chunksize - chunksize : (i + 1) * chunksize]
                )
            else:
                Dict["Chunk" + str(i)] = ";".join(
                    self.data[(i + 1) * chunksize - chunksize :]
                )
                return Dict

    def Chunklist(self):
        return [Chunk for Chunk in self.split_to_Chunk(self.chunksize)]

    def getValidation_table(self, Chunk):
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"
        post_fields = {
            "format": "json",
            "data": self.split_to_Chunk(self.chunksize)[Chunk],
        }
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
        df.insert(
            0,
            "OriginalVIN",
            pd.Series(self.split_to_Chunk(self.chunksize)[Chunk].split(";")),
        )
        print(f"{Chunk} is done!")
        return df

    def getThread_VT(self, Chunks):
        concat = pd.DataFrame()
        with concurrent.futures.ThreadPoolExecutor() as exe:
            results = exe.map(self.getValidation_table, self.Chunklist()[:Chunks])
        for result in results:
            concat = pd.concat([concat, result])
        return concat

    def getFor_VT(self, Chunks):
        concat = pd.DataFrame()
        for Chunk in self.Chunklist()[:Chunks]:
            result = self.getValidation_table(Chunk)
            concat = pd.concat([concat, result])
        return concat

    def getAll(self):
        concat = pd.DataFrame()
        with concurrent.futures.ThreadPoolExecutor() as exe:
            results = exe.map(self.getValidation_table, self.Chunklist())
        for result in results:
            concat = pd.concat([concat, result])
        return concat


# if __name__ == "__main__":
#     main()

