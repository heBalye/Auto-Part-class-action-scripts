import pandas as pd

ME_df = pd.read_excel(
    "C:\\Users\\FFR0103\\Desktop\\My files\\WORK\\Auto part\\QC process\\20191218\\NEW eligible vehicles to add 12.18.2019 per John's list.xlsx",
    dtype=str,
)

ME_df = ME_df.dropna(how="all")
