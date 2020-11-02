import re
import pandas as pd

from geopy.geocoders import Nominatim, GoogleV3


def add_lat_long(row):
    """
    Adds latitude and longitude columns to a specific row of a dataframe
    
    Parameters
    ----------
    - `row : pd.Series`
        A row of a pandas dataframe
        
    Returns
    -------
    `pd.Series`
        The row passed in with additional latitude and longitude columns 
    """
    
    # My Google API key (please don't use mine)
    API_KEY = "AIzaSyC2CFyh-OE27egOLMYdWyXoglF-aA4LET8"
    # Geolocator for geocoding address
    geolocator = GoogleV3(api_key=API_KEY, user_agent="DSV-WAV")
    # Splits on points in the street address that are necessary 
    # i.e. getting rid of suite numbers or stuff of the sort
    street = re.split("[,.]", row["street"])[0]
    # Construct the address
    address = ", ".join([street, row["city_state_zip"]])
    
    # See what address is
    print(address)
    
    # Geocode the address
    geocode = geolocator.geocode(address)
    # Add the new columns
    row["latitude"], row["longitude"] = geocode.latitude, geocode.longitude
    
    return row


def main():
    # The facility addresses
    facility_addresses = pd.read_csv("facility_addresses.csv")
    # Adding the latitude and longitude columns
    facility_addresses = facility_addresses.apply(add_lat_long, axis=1)
    # Dumping it to a csv
    facility_addresses.to_csv("facilities_geocoded.csv", index=False)
    
    
if __name__ == "__main__":
    main()