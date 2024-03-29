import multiprocessing
import os
import sys
import time

import pandas as pd
from PIL import Image
from pytesseract import Output, image_to_data

panoids = pd.read_csv(sys.argv[2])["panoid"].to_list()
files = [f"{sys.argv[1]}/{panoid}.jpg" for panoid in panoids]

# Language packs needed:
langs = [
    "eng",
    "chi_sim",
    "kor",
    "jpn",
    "tgl",
    "vie",
    "urd",
    "ben",
]


def get_ocr():
    def parse_file(file):
        output_prefix = os.path.splitext(os.path.basename(file))[0]

        if not os.path.exists(file):
            return None
        if os.path.exists(f"outputs/csvs/{output_prefix}__eng.csv"):
            print(f"Skipping {output_prefix}")
            return None

        print(f"Parsing {file}")
        start_time = time.time()
        with Image.open(file) as img:
            for lang in langs:
                data = image_to_data(img, lang, output_type=Output.DATAFRAME)
                end_time = time.time()
                data["lang"] = lang
                data["filename"] = file
                data["time"] = end_time - start_time
                data = data[data["conf"] > 70]
                data.to_csv(f"outputs/csvs/{output_prefix}__{lang}.csv", index=False)
        return None

    def parse_chunk(files):
        for file in files:
            parse_file(file)

    num_processes = 7
    chunk_size = len(files) // num_processes
    chunks = [files[i : i + chunk_size] for i in range(0, len(files), chunk_size)]

    processes = []
    for chunk in chunks:
        p = multiprocessing.Process(target=parse_chunk, args=(chunk,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


get_ocr()
