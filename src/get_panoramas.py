import concurrent.futures as cf
import os
import shutil
import sys

import pandas as pd

from points import stich_tiles

dirname = sys.argv[2]
if not os.path.exists(dirname):
    os.makedirs(dirname)

with open("outputs/filenames.txt", "r") as file:
    lines = file.readlines()

filenames = [line.strip() for line in lines]


def retrieve_panoramas(i, row):
    temp_folder = f"outputs/panoramas/temp/{row['panoid']}"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    filename = f"{row['panoid']}.jpg"
    if not os.path.exists(f"outputs/stitched/{filename}") and not filename in filenames:
        stich_tiles(row["panoid"], temp_folder, "outputs/stitched")
    shutil.rmtree(temp_folder)

    print(f"{i} images scraped")
    return i


if __name__ == "__main__":
    panoids = pd.read_csv(sys.argv[1])
    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        future_results = [
            executor.submit(retrieve_panoramas, i, row) for i, row in panoids.iterrows()
        ]
        for future in future_results:
            i = future.result()
