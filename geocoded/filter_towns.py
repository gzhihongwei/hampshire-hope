import json

from pathlib import Path
from geopy.geocoders import Nominatim


def filter_counties_towns(points, counties, cities):
    """
    Filters latitude, longitude points that are in `counties` or are in 
    `cities` if they are not in `counties`
    
    Parameters
    ----------
    `points` : `List[List[int, int]]`
        A list of latitude, longitude points
        
    `counties` : `List[str]`
        A list of county names to keep
    
    `cities` : `List[str]`
        A list of city names to keep that are not in counties
        
    Returns
    -------
    `List[List[int, int]]`
        List of latitude, logitude points that are in `counties` or in `cities`
    """
    # The geolocator used to get the address of a point
    geolocator = Nominatim(user_agent="DSV-WAV")
    # For logging purposes
    num = {"x": 0}
    
    def in_counties_towns(point):
        """
        Filter function that returns if `point` is in `counties` or `cities`
        
        Parameters
        ----------
        `point` : `List[int, int]`
            Latitude, longitude for a point
            
        Returns
        -------
        `bool`
            Boolean of whether `point` is in `counties` or `cities`
        """
        
        # Gets the address object of a point
        reverse = geolocator.reverse(point)
        # Gets the raw address information from Nominatim
        raw = reverse.raw["address"]
        # Increments number of points filtered
        num["x"] += 1

        # print(raw)
        # Logging for checking progress
        if "county" in raw:
            print(f'Number filtered so far: {num["x"]}, County: {raw["county"]}')
        
        # Keep point if it is in `counties`
        if "county" in raw and raw["county"] in counties:
            return True
        
        # Keep point if point is in a town, which is in `cities`
        if "town" in raw:
            return raw["town"] in cities
        
        # Keep point if point is in a city, which is in `cities`
        if "city" in raw:
            return raw["city"] in cities
        
        # Print out the raw address if none of the keys worked
        print(raw)
        
        # Point should be filtered out
        return False
    
    return list(filter(in_counties_towns, points))
    


def main():
    
    # List of towns of interest in Hampden county
    hampden_cities = [
        "Chicopee", "East Longmeadow", "Hampden", "Holyoke", 
        "Longmeadow", "Ludlow", "Palmer", "Westfield", 
        "West Springfield", "Wilbraham"
    ]
    
    # The list of unfiltered points
    unfiltered = json.load(open("points.json", "r"))
    
    # Keeps track where in `indices` we are
    start = 0
    
    # A file signaling which index of `indices` to start at
    next_start = Path("next_start.json")
    
    # Checks if we have a next_start index to start at
    if next_start.is_file():
        start = json.load(open("next_start.json", "r"))

    # Checks
    print(f"Start index of indices: {start}")
    
    # Split up the unfiltered points into 6 batches
    num_batches = 6
    
    # Gets a list of the indices to split the raw points into smaller sections
    indices = list()
    
    # Gets the indices to slice on
    for i in range(num_batches):
        indices.append(len(unfiltered) * i // num_batches)
    
    # Go from `start` to the length of `indices` - 1
    for i in range(start, len(indices)):
        # Slices the raw points based on the indices
        if i == 0:
            points = filter_counties_towns(unfiltered[: indices[i + 1]], ["Hampshire County"], hampden_cities)
        elif i == len(indices) - 1:
            points = filter_counties_towns(unfiltered[indices[i]:], ["Hampshire County"], hampden_cities)
        else:
            points = filter_counties_towns(unfiltered[indices[i]: indices[i + 1]], ["Hampshire County"], hampden_cities)
        
        # Obvious visual indicator
        print(f"\n Done with {i}\n")
        
        # Dump which index would be the start in range 
        json.dump(i + 1, open("next_start.json", "w"))
      
        # If we already have a filtered.json file
        if Path("filtered.json").is_file():
            # Loads all of the points we have filtered so far
            filtered_points = json.load(open("filtered.json", "r"))
            # Add new filtered points to the list
            filtered_points.extend(points)
        else:
            # The file does not exist
            filtered_points = points
             
        # Dump/redump the filtered points
        json.dump(filtered_points, open("filtered.json", "w"))
        
    next_start.unlink()

if __name__ == "__main__":
    main()
    