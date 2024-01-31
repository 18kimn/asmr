import os
import re

import geopandas as gp
import pandas as pd

borders = gp.read_file("inputs/Detroit_Boxes.geojson")


def points_contains(points_filename):
    df = pd.read_csv(points_filename, low_memory=False, on_bad_lines="skip")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce", downcast="float")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce", downcast="float")
    gdf = gp.GeoDataFrame(
        df, geometry=gp.points_from_xy(df.lon, df.lat), crs="EPSG:4326"
    )
    points_within = gp.sjoin(gdf, borders, predicate="within")
    return points_within, df.shape[0]


def run_search():
    filenames = os.listdir("outputs/Panoids")
    filtered_filenames = []
    for f in filenames:
        if re.search("AllPanoids.*csv$", f):
            filtered_filenames.append(f)

    points = []
    totalRows = 0
    matchedRows = 0
    i = 0
    for filename in filtered_filenames:
        i += 1
        print(f"{filename} ({i}/{len(filtered_filenames)})")
        result, rows = points_contains("outputs/Panoids/" + filename)
        totalRows = totalRows + rows
        matchedRows = matchedRows + result.shape[0]
        if result.shape[0]:
            points.append(result)

    points = pd.concat(points, axis=0, ignore_index=False)
    return points, totalRows, matchedRows


result, totalRows, matchedRows = run_search()
print(f"{matchedRows}/{totalRows} PanoIDs are within bounding polygons")
result.to_csv("outputs/filtered_panoids.csv", index=False)
