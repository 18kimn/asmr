import sys

import geopandas as gp
import osmnx as ox
from shapely.geometry import MultiPolygon, Point

DETROIT_CRS = "EPSG:26990"

if __name__ == "__main__":
    bounds = gp.read_file(sys.argv[1])
    bounds = MultiPolygon(bounds["geometry"].tolist())

    # Get network of streets/roads
    graph = ox.graph_from_polygon(polygon=bounds, network_type="all_private", retain_all=True)

    # Interpolate points along them
    edges = ox.graph_to_gdfs(graph, nodes=False)
    generators = edges.to_crs(DETROIT_CRS)["geometry"].apply(
        lambda line: ox.utils_geo.interpolate_points(geom=line, dist=25)
    )

    points = []
    for generator in generators:
        for x, y in generator:
            points.append(Point(x, y))

    edges_gdf = gp.GeoDataFrame(points, columns=["geometry"], crs=DETROIT_CRS).to_crs(
        "EPSG:4326"
    )
    edges_gdf["x"] = edges_gdf["geometry"].x
    edges_gdf["y"] = edges_gdf["geometry"].y

    edges_gdf[["x", "y"]].drop_duplicates().to_csv(sys.argv[2], index=False)
