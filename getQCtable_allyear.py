import pandas as pd
import numpy as np

from Dictionary import dictionary
from Eiligble_table import ME_df
from getMatch import getMatch
from getModel_Year_MakeID import getModel_Year_MakeID


def getQCtable_allyear(Make_id, Year):

    QC_Make = pd.DataFrame()

    Years = list(ME_df[ME_df.Make.str.lower() == dictionary[Make_id]].Year.unique())

    for Year in Years:

        Match_list = getMatch(Make_id, Year,)

        TopMatch = [rec[0].split(":")[0] for rec in Match_list]

        QC_Make_Year = ME_df[
            (ME_df.Make.str.lower() == dictionary[Make_id]) & (ME_df.Year == Year)
        ].sort_values(by=["Make", "Year", "Model"])

        QC_Make_Year["TopMatch"] = TopMatch

        QC_Make_Year["MatchOptions"] = Match_list

        QC_Make_Year["Match"] = np.where(
            QC_Make_Year.Model.str.lower() == QC_Make_Year.TopMatch.str.lower(),
            "Yes",
            "No",
        )

        QC_Make_Year["HighestScore"] = [
            int(rec[0].split(": ")[1]) if type(rec) != str else "N/A"
            for rec in QC_Make_Year["MatchOptions"]
        ]

        QC_Make_Year["TopMaTchExsting"] = [
            np.where(
                QC_Make_Year["TopMatch"].values[i].lower()
                in QC_Make_Year.Model.str.lower().unique(),
                "Yes",
                "No",
            )
            if QC_Make_Year["HighestScore"].values[i] >= 80
            else "No"
            for i in range(len(QC_Make_Year["TopMatch"]))
        ]

        QC_Make = pd.concat([QC_Make, QC_Make_Year])

    return QC_Make
