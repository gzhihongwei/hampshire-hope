import itertools
import json
import numpy as np

from pathlib import Path
from geopy.geocoders import Nominatim


def bounding_box_to_points(min_lat, max_lat, min_long, max_long, num_lat, num_long):
    """
    Function that converts a bounding box to `num_x` * `num_y` points within
    the bounding box.
    
    Parameters
    ---
    - min_lat: minimum longitude
    - max_lat: maximum longitude
    - min_long: minimum Longitude
    - max_long: maximum longitude
    - num_lat: number of points along latitude
    - num_long: number of points along longitude
    
    Return
    ---
    - points: list of tuples of (latitude, longitude)
    """
    
    # Gets evenly spaced latitude values, and `num_lat` of them
    latitudes = np.linspace(min_lat, max_lat, num=num_lat)
    # Gets evenly spaced longitude values, and `num_long` of them
    longitudes = np.linspace(min_long, max_long, num=num_long)
    # Cartesian product of the latitudes and longitudes as a list
    points = list(itertools.product(latitudes, longitudes))
    
    return points


def filter_points(points, counties):
    """
    Filters to a list of latitude, longitude points that are in counties
    
    Parameters
    ---
    - `points`: Tuple of floats, specifically (latitude, longitude)
    - `counties`: List of strings, each string being a county in the USA
    
    Return
    ---
    Returns the tuples of latitude, longitude points that are in the specified counties
    """
    
    # OpenStreetMap's open geocoding API
    geolocator = Nominatim(user_agent="DSC-WAV")
    # Logs how many points have been geocoded and compared
    num = {"x": 0}
    
    def filter_counties(point):
        """
        Filter function that returns `True` if `point` is in one of the counties
        
        Parameters
        ---
        - `point`: Tuple of latitude and longitude
        
        Return
        ---
        Returns a boolean of whether `point` is in any of the counties
        """
        
        # Reverse geocoding the point and gets exactly one result
        location = geolocator.reverse(point, exactly_one=True)
        # Gets the Nominatim raw dictionary from the result
        address = location.raw["address"]
        
        # Don't care if the entry does not have a county associated with it
        if "county" not in address:
            return False
        
        # Get's the county of `point`
        county = address["county"]
        # Logging for visuals of which county
        print(county)
        # Increments number of counties geocoded
        num["x"] += 1
        # Logs for visuals of how many counties have been geocoded
        print(num["x"])
        # Returns if county is in counties
        return county in counties
    
    # Returns list of the filtered points that are in `counties`
    return list(filter(filter_counties, points))


def main():
    
    # Load raw points if they exist
    raw_points_file = Path("raw_points.json")
    
    if not raw_points_file.is_file():
        # Gets the bounding boxes for Hampshire
        geolocator = Nominatim(user_agent="DSC-WAV")
        hampshire = geolocator.geocode("Hampshire County, MA")
        hampshire_bb = list(map(float, hampshire.raw['boundingbox']))
        # Gets the bounding boxes for Hampden
        hampden = geolocator.geocode("Hampden County, MA")
        hampden_bb = list(map(float, hampden.raw['boundingbox']))

        # Gets the points in the bounding boxes for each county
        hampshire_points = bounding_box_to_points(*hampshire_bb, 32, 32)
        hampden_points = bounding_box_to_points(*hampden_bb, 32, 32)
        
        # Counties to consider
        counties = ["Hampshire County", "Hampden County"]

        # Dumps all of the points into a json file called "raw_points.json"
        json.dump(hampshire_points + hampden_points, open('raw_points.json', 'w'))
    
    # Gets all of the raw points
    raw_points = json.load(open("raw_points.json", "r"))
    
    # Signal to user
    print("Raw points loaded")
    
    # Keeps track where in `indices` we are
    start = 0
    
    # A file signaling which index of `indices` to start at
    next_start = Path("next_start.json")
    
    # Checks if we have a next_start index to start at
    if next_start.is_file():
        start = json.load(open("next_start.json", "r"))

    # Checks if start changed
    print(f"Start index of indices: {start}")
    
    # Gets a list of the indices to split the raw points into smaller sections
    indices = list()
    
    # Number of batches to split points into
    num_batches = 6
    
    # I chose 5 batches in this case
    for i in range(num_batches):
        indices.append(len(raw_points) * i // num_batches)
    
    # I adjusted the start of this range because sometimes Nominatim crashed
    for i in range(start, len(indices)):
        # Slices the raw points based on the indices
        if i == 0:
            points = filter_points(raw_points[:indices[i + 1]], counties)
        elif i == len(indices) - 1:
            points = filter_points(raw_points[indices[i]:], counties)
        else:
            points = filter_points(raw_points[indices[i]: indices[i + 1]], counties)
        
        # Obvious visual indicator
        print(f"\n Done with {i}\n")
        
        # Dump which index would be the start in range 
        json.dump(i + 1, open("next_start.json", "w"))
        
        # Loads all of the points we have filtered so far
        # Intially I had `points.json` be an empty list
        points_so_far = json.load(open("points.json", "r"))
        # Add new filtered points to the list
        points_so_far.extend(points)
        # Redump the filtered points
        json.dump(points_so_far, open("points.json", "w"))
    
    # Delete unnecessary files
    raw_points_file.unlink()
    next_start.unlink()
    
if __name__ == "__main__":
    main()