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

    def __len__(self):
        return len(self.data)

    # Create chunk that contains vins in size of chunksize
    def split_to_Chunk(self, chunksize):
        Dict = {}
        for i in range(len(self.data) // chunksize + 1):
            if (i + 1) * chunksize < len(self.data):
                Dict["Chunk" + str(i)] = ";".join(
                    self.data[i * chunksize : (i + 1) * chunksize]
                )
            else:
                Dict["Chunk" + str(i)] = ";".join(self.data[i * chunksize :])
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
        if r.ok:
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
            print(f"{Chunk} is done! Total: {len(self.data) // self.chunksize - 1}\n")

        else:
            print(
                f'The Status code: {r.status_code}, The input data is: {post_fields["data"]}, The Chunk name is {Chunk}\n Second attempt: trying to split and run one by one.....'
            )
            df = pd.DataFrame()
            for singleVIN in self.split_to_Chunk(self.chunksize)[Chunk].split(";"):
                post_fields = {
                    "format": "json",
                    "data": singleVIN,
                }
                r = requests.post(url, data=post_fields)

                if r.ok:
                    result = json.loads(r.text)
                    temp = pd.DataFrame(result["Results"])[
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
                    temp.insert(
                        0, "OriginalVIN", [singleVIN],
                    )
                    df = pd.concat([df, temp])
                    print(f"Successfully get the VIN: {singleVIN} \n")
                else:
                    print(
                        f"Second attampt failed... status: {r.status_code}.\n Please Manaually try this VIN: {singleVIN}\n"
                    )
                    df = pd.DataFrame([singleVIN], columns=["OriginalVIN"])

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

