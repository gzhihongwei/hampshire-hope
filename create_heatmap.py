"""
Massachusetts shapefile sources:
    - town borders: https://docs.digital.mass.gov/dataset/massgis-data-community-boundaries-towns-survey-points
    - county borders: https://docs.digital.mass.gov/dataset/massgis-data-county-boundaries
"""

import json
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import pandas as pd
from dbfread import DBF
import stateplane
import random
import math

MASS_SHP_X_RANGE = (19012.018500000006, 345695.33150000003)
MASS_SHP_Y_RANGE = (768402.6535, 968859.0965)


def get_reference_points(filepath):
    with open(filepath) as points_json:
        reference_points = json.load(points_json)

    return reference_points

def plot_mass_heatmap(points_dataframe,heat_feature_col):
    # convert .shp files into GeoDataFrames
    mass_counties = gpd.read_file('./map_files/mass_counties/COUNTIES_POLY.shp')  # mass county borders
    mass_tows = gpd.read_file('./map_files/mass_towns/TOWNSSURVEY_POLY.shp')  # mass town borders

    # create base matplotlib plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # plot mass shape
    mass_counties.plot(ax=ax, figsize=(10, 10), alpha=0.5, edgecolor='black', facecolor='red')

    # plot filtered points
    points_dataframe.plot(ax=ax, cmap='viridis', column=heat_feature_col, legend=True)

    # plot town and county borders on top
    mass_tows.plot(ax=ax, figsize=(10, 10), alpha=1, edgecolor='yellow', color='none')
    mass_counties.plot(ax=ax, figsize=(10, 10), alpha=1, edgecolor='black', facecolor='none')

    # show plot
    plt.show()

def main():
    # load in reference points from json
    reference_points = get_reference_points('./my_test_data/points.json')

    # convert latitude and longitude of each coordinate to the State Plane Coordinate System (SPC) for
    # compatibility with the Massachusetts shapefiles
    x_coords = []
    y_coords = []
    latitudes = []
    longitudes = []
    for lat, lon in reference_points:
        x, y = stateplane.from_latlon(lat, lon)

        # disregard points outside of Massachusetts on actual geopandas plot map
        if x < MASS_SHP_X_RANGE[0] or x > MASS_SHP_X_RANGE[1] or y < MASS_SHP_Y_RANGE[0] or y > MASS_SHP_Y_RANGE[1]:
            print(f'converted SPC coord outside of massachusetts: lat,lon={(lat, lon)}, SPC x,y coords={(x, y)}')
            continue

        x_coords.append(x)
        y_coords.append(y)
        latitudes.append(lat)
        longitudes.append(lon)

    # create column to use as heat variable for testing
    random_prices = [x for x in x_coords]

    # create geopandas dataframe from point tuples for geopandas plotting
    df = pd.DataFrame({'x': x_coords,
                       'y': y_coords,
                       'price': random_prices})
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))

    # plot heatmap based on price column of geopandas dataframe
    plot_mass_heatmap(points,'price')

    # # get box coords of geoplot mass map
    # print(f'mass geoplot map x coords range: {ax.get_xlim()}')
    # print(f'mass geoplot map y coords range: {ax.get_ylim()}')

    # # read in county names from .dbf file
    # table = DBF('./map_files/mass_counties/COUNTYNC_POLY.dbf')
    # for record in table:
    #     print(record)
    #
    # table2 = DBF('./map_files/mass_towns/TOWNSSURVEY_POLY.dbf')
    # for i, record in enumerate(table2):
    #     print(i, record)
    #
    # table3 = DBF('./map_files/min1latlong/MINLL1_ARC.dbf')
    # for i, record in enumerate(table3):
    #     print(i, record)




if __name__ == '__main__':
    main()
