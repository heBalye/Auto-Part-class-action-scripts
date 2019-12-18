import json

import httplib2
import pandas as pd
from fuzzywuzzy import process

from Dictionary import dictionary
from Eiligble_table import ME_df
from getModel_Year_MakeID import getModel_Year_MakeID


def getMatch(Make_id, Year):
    Rlist = []

    try:
        Valid_df = getModel_Year_MakeID(Make_id, Year)

    except:
        QC_Make_year = ME_df[
            (ME_df.Make.str.lower() == dictionary[Make_id]) & (ME_df.Year == Year)
        ].sort_values(by=["Make", "Year", "Model"])

        Rlist = ["No Such year in the Database"] * len(QC_Make_year)
    else:
        QC_Make_year = ME_df[
            (ME_df.Make.str.lower() == dictionary[Make_id]) & (ME_df.Year == Year)
        ].sort_values(by=["Make", "Year", "Model"])

        for i in range(len(QC_Make_year.Model)):
            str2Match = str(QC_Make_year.Model.values[i])
            strOptions = [z for z in Valid_df.Model_Name]
            Ratios = process.extract(str2Match, strOptions)
            Rlist.append([a + ": " + str(dict(Ratios)[a]) for a in dict(Ratios)])

    return Rlist
