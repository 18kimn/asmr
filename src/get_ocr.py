import concurrent.futures as cf
import io
import os
import sys
import time

import pandas as pd
from PIL import Image
from pytesseract import Output, image_to_data

files = os.listdir(sys.argv[1])[:1000]

# Language packs needed:
langs = [
    "eng",
    "chi_sim_vert",
    "chi_sim",
    "chi_tra",
    "kor",
    "kor_vert",
    "jpn",
    "jpn_vert",
    "tgl",
    "vie",
    "urd",
    "ben",
]


def get_ocr():
    def parse_file(file):
        if os.path.exists(os.path.join(f"outputs/csvs/{file}__en.csv")):
            return None

        start_time = time.time()
        with Image.open(os.path.join("outputs/stitched", file)) as img:
            for lang in langs:
                data = image_to_data(
                    img, lang, output_type=Output.DATAFRAME, config="--psm 12"
                )
                end_time = time.time()
                data["lang"] = lang
                data["filename"] = file
                data["time"] = end_time - start_time
                data = data[data["conf"] > 70]
                data.to_csv(f"outputs/csvs/{file}__{lang}.csv", index=False)
        return None

    with cf.ThreadPoolExecutor(max_workers=4) as executor:
        future_results = [executor.submit(parse_file, file) for file in files]
        for i, _ in future_results:
            print("{i}th photo parsed")


get_ocr()
