import unittest

import pandas as pd

from APIValidation.CleanVIN import Col_to_str, ValidationProcess


# test data
Test_dir = (
    r"C:\Users\FFR0103\Desktop\My files\Python Project\Auto Part\API validation\test"
)

Test_filename = r"\Testcase.xlsx"

test_df = pd.read_excel(Test_dir + Test_filename, dtype=str, header=0,)

# # print(test_df)


class TestCleanVIN(unittest.TestCase):
    def setUp(self):
        self.test_process = ValidationProcess(Col_to_str(test_df, "VIN", ";"), 4)

    # check the len if match
    def test_len(self):
        self.assertEqual(len(self.test_process), len(test_df))

    # Check the VIN from process output is the same as input
    def test_match(self):
        VIN_process = list(self.test_process.getAll().iloc[:, 0].values)
        VIN_df = list(test_df.iloc[:, 0].values)
        self.assertEqual(VIN_process, VIN_df)


if __name__ == "__main__":
    unittest.main()
