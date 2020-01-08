import glob

import pandas as pd

FileName = glob.glob(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\Mattress Firm\\Source\\*.*"
)


df = pd.read_excel(FileName[1], sheet_name=None)
print(
    df["CC"]
    .iloc[0, :]
    .str.contains("state|vin", regex=True, case=False, na=False)
    .sum()
)

