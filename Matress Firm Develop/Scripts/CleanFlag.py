import re

import pandas as pd

table = pd.read_excel(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\Mattress Firm\\Output\\CleanOutputformatted.xlsx"
)

Flag = pd.Series(None, index=range(len(table)))


for i, a in enumerate(table.StandardVIN.values):
    if re.match("(?=.*[0-9])(?=.*[a-zA-Z])", str(a)):
        Flag[i] = "Yes"
    else:
        Flag[i] = "No"

