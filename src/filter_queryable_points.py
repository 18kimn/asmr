import os
import re
import sys
import geopandas as gp
import pandas as pd

if __name__ == "__main__":
    borders = gp.read_file(sys.argv[1])
    df = pd.read_csv(sys.argv[2], low_memory=False, on_bad_lines="skip")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce", downcast="float")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce", downcast="float")
    gdf = gp.GeoDataFrame(
        df, geometry=gp.points_from_xy(df.lon, df.lat), crs="EPSG:4326"
    )
    points_within = gp.sjoin(gdf, borders, predicate="within")
    points_within.to_csv(sys.argv[3])