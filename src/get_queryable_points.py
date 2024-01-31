import os
import sys

import pandas as pd
from dotenv import load_dotenv

from points import panoids

load_dotenv()

if __name__ == "__main__":
    all_points = pd.read_csv(sys.argv[1])

    result = []
    for i, row in all_points.iterrows():
        print(
            f"{i}/{all_points.shape[0]} points queried; {len(result)} results retrieved"
        )
        coord_panoids = panoids(row["y"], row["x"], os.getenv("MAPS_API_KEY"))
        if coord_panoids:
            for panoid in coord_panoids:
                result.append(panoid)

    pd.DataFrame(result).drop_duplicates().to_csv(sys.argv[2], index=False)
