import glob
import sys

import pandas as pd


def aggregate_files(dir):
    ocrs = []
    csv_files = glob.glob(f"{dir}/*.csv")
    for csv_file in csv_files:
        ocr = pd.read_csv(csv_file, dtype=str)
        ocrs.append(ocr)

    ocr = pd.concat(ocrs, ignore_index=True)
    ocr.to_csv("outputs/ocr.csv", index=False)


aggregate_files(sys.argv[1])
