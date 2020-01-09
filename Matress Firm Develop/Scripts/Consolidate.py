import pandas as pd

df = pd.read_excel(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\Mattress Firm\\Output\\01062020\\QC_result_formatted_01062020.xlsx",
    sheet_name="Details",
    index_col=[0, 1],
)


StandardVIN = pd.Series(None, index=range(len(df)))

StandardState = pd.Series(None, index=range(len(df)))

df["# of  Value from selected VIN columns"] = 6 - df[
    df.columns[[4, 6, 7, 12, 13, 15]]
].isnull().sum(axis=1)


for i in range(len(df)):
    temp = []
    for val in df.iloc[i, [4, 6, 7, 12, 13, 15]]:
        if not pd.isnull(val):
            temp.append(str(val))
            StandardVIN[i] = ";".join(temp)


df["# of  values from selected State columns"] = 6 - df[
    df.columns[[5, 8, 9, 11, 16, 17]]
].isnull().sum(axis=1)
for i in range(len(df)):
    temp = []
    for val in df.iloc[i, [5, 8, 9, 11, 16, 17]]:
        if not pd.isnull(val):
            temp.append(str(val))
            StandardState[i] = ";".join(temp)

print(StandardState)
print(StandardVIN)
