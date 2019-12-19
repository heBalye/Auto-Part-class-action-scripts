import pandas as pd
from fuzzywuzzy import process


from getOptions import getOptions


def getMatch(Make_id, Year, Dict, ME_df):
    Rlist = []

    try:
        Options_list = getOptions(Make_id, Year)
        if len(getOptions(Make_id, Year)) == 0:
            raise Exception

    except:
        QC_Make_year = ME_df[
            (ME_df.Make.str.lower() == Dict[Make_id]) & (ME_df.Year == Year)
        ].sort_values(by=["Make", "Year", "Model"])

        Rlist = ["No Such Data in the vPIC Database"] * len(QC_Make_year)
    else:
        QC_Make_year = ME_df[
            (ME_df.Make.str.lower() == Dict[Make_id]) & (ME_df.Year == Year)
        ].sort_values(by=["Make", "Year", "Model"])

        for i in range(len(QC_Make_year.Model)):
            str2Match = str(QC_Make_year.Model.values[i])
            strOptions = Options_list
            Ratios = process.extract(str2Match, strOptions)
            Rlist.append([a + ": " + str(dict(Ratios)[a]) for a in dict(Ratios)])

    return Rlist

