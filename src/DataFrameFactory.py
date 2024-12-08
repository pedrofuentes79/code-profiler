from shapely.geometry import Point, Polygon
import numpy as np
import pandas as pd
import geopandas as gpd

pd.options.mode.copy_on_write = True


class DataFrameFactory:
    def generate_random_gdf(self, num_polygons, vertices, x_range, y_range):
        polygons = []
        for _ in range(num_polygons):
            points = [Point(np.random.uniform(*x_range), np.random.uniform(*y_range)) for _ in range(vertices)]
            polygon = Polygon([[p.x, p.y] for p in points])
            polygons.append(polygon)
        return gpd.GeoDataFrame(geometry=polygons)
    
    def generate_time_series_df(self, start_date, periods, freq):
        return pd.DataFrame({
            "msgTime": pd.date_range(start_date, periods=periods, freq=freq)
        })

    def generate_numeric_df_named(self, column_name, num_rows):
        return pd.DataFrame({
            column_name: np.random.random(num_rows)
        })
    
    def generate_large_df(self):
        return pd.DataFrame({
            "A": range(1000000),
            "B": range(1000000, 2000000),
            "C": range(2000000, 3000000)
        })