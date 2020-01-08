# This Script search all rows in the sheet and target down the possible header
import glob

import pandas as pd

FileName = glob.glob(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\Mattress Firm\\Source\\*.*"
)

print(len(FileName))
# init the Dict
Dict = {}
for i, file in enumerate(FileName):
    print("#of file", i)
    DF = pd.read_excel(file, sheet_name=None, header=None, dtype=str)
    Dict[file.split("\\")[-1]] = pd.DataFrame()
    for i, sheet in enumerate(DF):
        if len(DF[sheet]) > 0:
            for row in range(len(DF[sheet])):
                if (
                    DF[sheet]
                    .iloc[row, :]
                    .str.contains("state|vin", regex=True, case=False, na=False)
                    .sum()
                    > 0
                ):
                    df = pd.DataFrame(
                        {
                            "File Name": file.split("\\")[-1],
                            "Index of Sheet": i + 1,
                            "SheetName": [str(sheet)],
                            "Row number contains 'V/S'": [str(row + 1)],
                        }
                    )
                    break
                df = pd.DataFrame(
                    {
                        "File Name": file.split("\\")[-1],
                        "Index of Sheet": i + 1,
                        "SheetName": [str(sheet)],
                        "Row number contains 'V/S'": ["NO VIN or State"],
                    }
                )
        else:
            df = pd.DataFrame(
                {
                    "File Name": file.split("\\")[-1],
                    "Index of Sheet": i + 1,
                    "SheetName": [str(sheet)],
                    "Row number contains 'V/S'": ["Empty Sheet"],
                }
            )
        Dict[file.split("\\")[-1]] = pd.concat(
            [Dict[file.split("\\")[-1]], df], sort=False
        )
QC_table = pd.concat(Dict, sort=False)

Output_loc = input("enter the location of output folder")

QC_table.to_excel(
    Output_loc, index=True, header=True,
)

