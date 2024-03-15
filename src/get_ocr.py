import concurrent.futures as cf
import io
import os
import sys
import time

import pandas as pd
from PIL import Image
from pytesseract import image_to_data

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
        start_time = time.time()
        with Image.open(os.path.join("outputs/stitched", file)) as img:
            data = image_to_data(img)
            end_time = time.time()
            data = pd.read_csv(io.StringIO(data), sep="\t")
            data = data[["left", "top", "width", "height", "conf", "text"]]
            data["filename"] = file
            data["time"] = end_time - start_time
        return data

    data_list = []
    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        future_results = [executor.submit(parse_file, file) for file in files]
        for future in future_results:
            data_list.append(future.result())

    data = pd.concat(data_list)
    data = data[data["text"].notna()]
    data.to_csv("outputs/raw_ocr.csv", index=False)


get_ocr()
