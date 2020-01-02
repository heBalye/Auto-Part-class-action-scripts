import pandas as pd
import numpy as np

from getMatch import getMatch


def getQCtable_allyear(ME_df, Dict):

    row_number = 1

    QC_Make = pd.DataFrame()

    for Make_id in Dict:
        Years = list(ME_df[ME_df.Make.str.lower() == Dict[Make_id]].Year.unique())

        for Year in Years:

            Match_list = getMatch(Make_id, Year, Dict, ME_df)

            TopMatch = [
                rec[0].split(":")[0] if len(rec) > 0 and type(rec) == list else "N/A"
                for rec in Match_list
            ]

            QC_Make_Year = ME_df[
                (ME_df.Make.str.lower() == Dict[Make_id]) & (ME_df.Year == Year)
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
            # IfExisting feature:
            #             QC_Make_Year["TopMaTchExsting"] = [
            #                 np.where(
            #                     QC_Make_Year["TopMatch"].values[i].lower()
            #                     in QC_Make_Year.Model.str.lower().unique(),
            #                     "Yes",
            #                     "No",
            #                 )
            #                 if QC_Make_Year["HighestScore"].values[i] >= 80
            #                 else "No"
            #                 for i in range(len(QC_Make_Year["TopMatch"]))
            #             ]

            QC_Make = pd.concat([QC_Make, QC_Make_Year])
            print(row_number, Make_id, Dict[Make_id], Year)
            row_number += 1

    return QC_Make


test = {
    475: "acura",
    493: "alfa romeo",
    582: "audi",
    603: "ferrari",
    "N/A": "scion",
}
from Eiligble_table import ME_df

print(getQCtable_allyear(ME_df, test))

