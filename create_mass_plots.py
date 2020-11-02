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
from geopy.geocoders import Nominatim

MASS_FIPS_CODE = 25
MASS_COUNTIES_COORDS_PATH = "./map_files/mass_counties_coords.csv"
MASS_TOWNS_COORDS_PATH = "./map_files/mass_towns_coords.csv"
REFERENCE_POINTS_PATH = "./Points/points.json"
MASS_GOV_COUNTIES_DATA = "./map_files/mass_counties/COUNTIES_POLYM.dbf"
MASS_GOV_TOWNS_DATA = "./map_files/mass_towns/TOWNSSURVEY_POLYM.dbf"
MASS_COUNTIES_SHAPEFILE_PATH = "./map_files/mass_counties/COUNTIES_POLYM.shp"
MASS_TOWNS_SHAPEFILE_PATH = "./map_files/mass_towns/TOWNSSURVEY_POLYM.shp"


class MassPlot:
    def __init__(self):
        """
        Class for creating heatmaps, Choropleths, and other types of maps of Massachusetts with GeoPandas and geoplot
        """

        self.geolocator = Nominatim(user_agent='DSV-WAV')

        # convert shapefiles of massachusetts separated by counties and towns, and convert them to
        # GeoDataFrames from their respective shapefiles
        self.mass_counties_geoframe = gpd.read_file(MASS_COUNTIES_SHAPEFILE_PATH)  # county borders
        self.mass_towns_geoframe = gpd.read_file(MASS_TOWNS_SHAPEFILE_PATH)  # town borders

        # add column to GeoDataFrames for centroid points of mass counties and towns
        self.mass_counties_geoframe['center'] = self.mass_counties_geoframe['geometry'].centroid
        self.mass_towns_geoframe['center'] = self.mass_towns_geoframe['geometry'].centroid

        # add column to GeoDataFrames for lat/lon and SPCS coords of centroids and labels for mass counties and towns
        counties_df = self._get_town_coords(counties=True)
        self.mass_counties_geoframe = pd.concat((self.mass_counties_geoframe, counties_df), axis=1)
        towns_df = self._get_town_coords()
        self.mass_towns_geoframe = pd.concat((self.mass_towns_geoframe, towns_df), axis=1)

    def plot_mass_heatmap(self, points_dataframe, heat_feature_col, plot_attr=None):
        """
        Plot a heatmap of mass based on given reference points dataframe and a column variable to use as "heat"

        :param points_dataframe: (GeoDataFrame) dataframe of reference points data
        :param heat_feature_col: (str) name of column in points_dataframe to use as the "heat" variable for heatmap
        :param plot_attr: optional dictionary of plot attributes
        """

        # define default plot attributes
        default_plot_attr = {
            'base_edgecolor': 'black',
            'base_facecolor': 'red',
            'base_alpha': 0.5,
            'county_borders': True,
            'town_borders': True,
            'county_border_color': 'yellow',
            'town_border_color': 'black',
            'county_border_alpha': 1,
            'town_border_alpha': 1,
            'plot_title': 'Example Hampshire County HeatMap',
            'legend_label': heat_feature_col,
            'county_names': True,
            'town_names': True,
            'county_names_color': '#FFDE00',  # darkish yellow kinda
            'town_names_color': 'black',
            'county_names_alpha': 1,
            'town_names_alpha': 1,
            'county_names_fontsize': 'large',
            'town_names_fontsize': 'xx-small',
            'county_names_fontweight': 'bold',
            'town_names_fontweight': 'normal',
        }

        # update default plot attributes with ones passed to method
        if plot_attr:
            default_plot_attr.update(plot_attr)

        # plot base mass map and get its box bounds
        fig, ax = self._plot_mass(default_plot_attr)

        # # disregard points outside of Massachusetts on actual geopandas plot map due to SPCS conversion
        # x_bounds = ax.get_xlim()
        # y_bounds = ax.get_ylim()
        # bad_points = []
        # for row in points_dataframe.itertuples():
        #     i, x, y = row.Index, row.x, row.y
        #     if x < x_bounds[0] or x > x_bounds[1] or y < y_bounds[0] or y > y_bounds[1]:
        #         lat, lon = stateplane.to_latlon(x, y, abbr='MA_M')
        #         print(row)
        #         print(f'converted SPCS coord outside of massachusetts: lat,lon={(lat, lon)}, SPC x,y coords={(x, y)}')
        #         bad_points.append(i)
        # points_dataframe = points_dataframe.drop(labels=bad_points,axis=0)

        # plot heatmap points
        points_dataframe.plot(ax=ax, cmap='viridis', column=heat_feature_col, legend=True,
                              legend_kwds={'label': default_plot_attr['legend_label']})

        # plot town labels
        if default_plot_attr['town_names']:
            for row in self.mass_towns_geoframe.itertuples():
                if pd.isna(row.town):
                    continue
                x, y = row.centroid_x, row.centroid_y
                ax.annotate(row.town, xy=(x, y), horizontalalignment='center', verticalalignment='center',
                            fontsize=default_plot_attr['town_names_fontsize'],
                            alpha=default_plot_attr['town_names_alpha'],
                            color=default_plot_attr['town_names_color'],
                            fontweight=default_plot_attr['town_names_fontweight'])

        # plot county labels
        if default_plot_attr['county_names']:
            for row in self.mass_counties_geoframe.itertuples():
                x, y = row.centroid_x, row.centroid_y
                ax.annotate(row.county, xy=(x, y), horizontalalignment='center', verticalalignment='center',
                            fontsize=default_plot_attr['county_names_fontsize'],
                            alpha=default_plot_attr['county_names_alpha'],
                            color=default_plot_attr['county_names_color'],
                            fontweight=default_plot_attr['county_names_fontweight'])

        # plot town and county borders on top of heatmap points
        if default_plot_attr['town_borders']:
            self.mass_towns_geoframe.plot(ax=ax, figsize=(10, 10), color='none',
                                          alpha=default_plot_attr['town_border_alpha'],
                                          edgecolor=default_plot_attr['town_border_color'])
        if default_plot_attr['county_borders']:
            self.mass_counties_geoframe.plot(ax=ax, figsize=(10, 10), facecolor='none',
                                             alpha=default_plot_attr['county_border_alpha'],
                                             edgecolor=default_plot_attr['county_border_color'])

        ax.set_title(default_plot_attr['plot_title'])

        # show plot
        plt.show()

    def save_mass_coords_csv(self, counties=True, towns=True):
        """
        Generate and save mass town and/or county coords to mass_towns_coords.csv and/or
        mass_counties_coords.csv respectively, this will make calls to subsequent calls to _get_town_coords()
        much faster when from_file='csv' since points will not need to be generated by geopy

        :param counties: (bool) indicates whether county coords should be saved to disk
        :param towns: (bool) indicates whether town coords should be saved to disk
        """

        if counties:
            self._get_town_coords(counties=True, from_file='shp', save_to_csv=True)
        if towns:
            self._get_town_coords(from_file='shp', save_to_csv=True)

    def _plot_mass(self, plot_attr):
        """
        Plots and returns a base plot of Massachusetts' shape

        :param plot_attr: dictionary of plot attributes
        :return: matplotlib figure and axes objects
        """
        # create base matplotlib plot
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        # plot mass shape based off one of the GeoDataFrames, does not matter which to get base mass shape
        self.mass_counties_geoframe.plot(ax=ax, figsize=(10, 10), alpha=plot_attr['base_alpha'],
                                         edgecolor=plot_attr['base_edgecolor'],
                                         facecolor=plot_attr['base_facecolor'])

        return fig, ax

    def _get_town_coords(self, counties=False, from_file='csv', save_to_csv=False):
        """
        Reads in and creates dictionary of mass town lat/lon and SPCS coords from file type specified with from_file,
        and save to file at MASS_TOWNS_COORDS_PATH if save_to_csv is true. If counties is true the same process is
        done except with mass counties instead of towns.

        :param counties: (bool) indicates whether to generate coords for counties or towns
        :param from_file: (str) file type abbreviation which decides how coords are generated
                        - 'csv', gets points from mass_towns_coords.csv or mass_counties_coords.csv
                        - 'shp', generates points with geopy from from centroids of mass towns shapefile's polygons
                        - 'dbf', generates points with geopy from mass.gov database (.dbf) file (not accurate
                            with respect to mass county borders when counties=True), will also save to specific
                            mass_towns_coords_dbf.csv or mass_counties_coords_dbf.csv file. Should be used
                            for saving coords based on dbf file and not used to map county or town labels to
                            self.mass_counties_geoframe or self.mass_towns_geoframe
        :param save_to_csv: (bool) indicates whether generated points will be saved to a csv file on disk
        :return: coordinates dictionary of towns or counties label where each label maps to another dictionary with
                 keys 'lat','lon','x', and 'y'
        """

        towns_df = None

        # convert mass_towns_coords.csv to pandas dataframe
        if from_file == 'csv':
            path = MASS_TOWNS_COORDS_PATH if not counties else MASS_COUNTIES_COORDS_PATH
            towns_df = pd.read_csv(path)

        # generate points with geopy
        else:
            names = []
            centroid_x = []
            centroid_y = []
            centroid_lat = []
            centroid_lon = []

            # use geopy to get town coords from centroids of shapefile polygons
            if from_file == 'shp':
                gdf = self.mass_towns_geoframe if not counties else self.mass_counties_geoframe
                for row in gdf.itertuples():
                    x, y = row.center.x, row.center.y  # SCPS coords
                    lat, lon = stateplane.to_latlon(x, y, abbr='MA_M')

                    location = self.geolocator.reverse(f"{lat}, {lon}")

                    if not counties:
                        # get name of town, city, or village
                        address_dict = location.raw['address']
                        if 'town' in address_dict:
                            town_name = address_dict['town']
                        elif 'city' in address_dict:
                            town_name = address_dict['city']
                        elif 'village' in address_dict:
                            town_name = address_dict['village']
                        else:
                            print('Unable to get town, city, or village name from location at centroid point '
                                  f'from shapefile with info:\n{address_dict}')
                    else:
                        # get county name
                        town_name = location.raw['address']['county']

                    names.append(town_name)
                    centroid_x.append(x)
                    centroid_y.append(y)
                    centroid_lat.append(lat)
                    centroid_lon.append(lon)

            # use geopy to get town coords from mass.gov database (.dbf) file
            elif from_file == 'dbf':
                path = MASS_GOV_TOWNS_DATA if not counties else MASS_GOV_COUNTIES_DATA

                # read in towns data from database file (.dbf) from mass.gov
                mass_gov_towns_data = DBF(path)

                # loop through rows of database file and get lat/lon and SPCS coords of town
                key = 'TOWN' if not counties else 'COUNTY'
                seen = set()
                for row in mass_gov_towns_data:
                    if row[key] not in seen:
                        town_name = row[key]

                        location = self.geolocator.geocode(f'{town_name} MA')
                        lat, lon = location.latitude, location.longitude
                        x, y = stateplane.from_latlon(lat, lon, statefp=MASS_FIPS_CODE)  # SCPS coords

                        names.append(town_name)
                        centroid_x.append(x)
                        centroid_y.append(y)
                        centroid_lat.append(lat)
                        centroid_lon.append(lon)

                        seen.add(town_name)

            label_type = 'town' if not counties else 'county'
            towns_df = pd.DataFrame({label_type: names,
                                     'centroid_x': centroid_x,
                                     'centroid_y': centroid_y,
                                     'centroid_lat': centroid_lat,
                                     'centroid_lon': centroid_lon})

        if save_to_csv and towns_df is not None:
            path = MASS_TOWNS_COORDS_PATH if not counties else MASS_COUNTIES_COORDS_PATH
            towns_df.to_csv(path, index=False)

        return towns_df


def get_reference_points(filepath):
    with open(filepath) as points_json:
        reference_points = json.load(points_json)

    return reference_points


def main():
    # load in reference points from json
    reference_points = get_reference_points(REFERENCE_POINTS_PATH)

    # convert latitude and longitude of each coordinate to the State Plane Coordinate System (SPCS) for
    # compatibility with the Massachusetts shapefiles
    x_coords = []
    y_coords = []
    for lat, lon in reference_points:
        # set statefp to mass's FIPS code to prevent bad conversion from lat lon
        x, y = stateplane.from_latlon(lat, lon, statefp=MASS_FIPS_CODE)
        x_coords.append(x)
        y_coords.append(y)

    # create column to use as heat variable for testing
    random_prices = [x for x in x_coords]

    # create geopandas dataframe from point tuples for geopandas plotting
    df = pd.DataFrame({'x': x_coords,
                       'y': y_coords,
                       'price': random_prices})
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))

    # plot heatmap based on price column of geopandas dataframe
    mass_plot = MassPlot()
    mass_plot.plot_mass_heatmap(points, 'price', plot_attr={'legend_label': 'SPCS Coordinate System Easting Value'})


if __name__ == '__main__':
    main()
