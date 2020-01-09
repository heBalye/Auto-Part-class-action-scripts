import glob

import pandas as pd

QC_table = pd.read_excel(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\Mattress Firm\\Output\\123.xlsx",
    index_col=[0, 1],
)

test = QC_table[["File Name", "SheetName", "index of row contains 'V/S'"]].to_dict(
    orient="list"
)
header_dict = {}
sheet_dict = {}
for a, b, c in zip(
    test["File Name"], test["SheetName"], test["index of row contains 'V/S'"]
):
    #     print(a,b,c)
    temp = {}
    temp[b] = c
    if a not in header_dict:
        header_dict[a] = temp
    else:
        header_dict[a].update(temp)

