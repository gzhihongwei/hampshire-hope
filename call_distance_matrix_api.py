import requests
import json
import datetime
from datetime import timezone
import pandas as pd

# beginning of every API call to the Google Matrix API for json objects
URL_DIST = "https://maps.googleapis.com/maps/api/distancematrix/json?"


def call_distance_api(origins, destinations, key, arrival_year, arrival_month, arrival_day, arrival_hour=0):
    """
      Creates and calls a url for the Google Distance Matrix to retrieve the corresponding JSON object to the API call

      Documentation for Google Distance Matrix: https://developers.google.com/maps/documentation/distance-matrix/overview?authuser=2#DistanceMatrixRequests

      Parameters
      ---
      - origins: path to json file with an array of tuples containing latitude and longitude of origin points
      - destinations: path to json file with an array of tuples containing latitude and longitude of destination points
      - key: key for Google Cloud project needed for all calls to Google APIs
      Note: arrival_year, arrival_month, arrival_hour will only allow us to get useful information if
      the given year, month, and hour are within the next few weeks of the API call because Google doesn't
      provide information too far into the future and nothing from the past
      - arrival_year: year for arrival time (should be current year or upcoming year if API call is made towards
      the end of the current year)
      - arrival_month: month for arrival time (values 1-12)
      - arrival_day: day of the month for arrival time (values 1-31)
      - arrival_hour: hour of the day for arrival time (values 0-23)

      Return
      ---
      - json_object: contains the json object produced from the API call
      """
    file_origin = open(origins)
    file_dest = open(destinations)
    json_origin = json.load(file_origin)
    json_dest = json.load(file_dest)
    str_of_origin = ""
    str_of_dest = ""
    # creates a string of all the lats and longs of each origin point in the array of origins in the
    # form of lat,long|lat,long|...
    for origin in json_origin:
        str_of_origin += str(origin[0]) + "," + str(origin[1]) + "|"
    # creates a string of all the lats and longs of each destination point in the array of destinations in the
    # form of lat,long|lat,long|...
    for dest in json_dest:
        str_of_dest += str(dest[0]) + "," + str(dest[1]) + "|"

    # removes the last | from both strings
    str_of_origin = str_of_origin[:-1]
    str_of_dest = str_of_dest[:-1]

    # converts given year, month, hour to UTC time; assumes day as the 1st of the given month and minute and second at 0
    time = datetime.datetime(year=arrival_year, month=arrival_month, day=arrival_day, hour=arrival_hour, minute=0,
                             second=0)
    utc_time = time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    # formats final URL for the API call
    final_url = URL_DIST \
                + "units=imperial" + \
                "&origins=" + str_of_origin + \
                "&destinations=" + str_of_dest + \
                "&mode=transit" + \
                "&arrival_time=" + str(utc_timestamp)[:-2] \
                + "&key=" + key

    # prints final URL for testing purposes
    print(final_url)

    # requests given URL
    req = requests.get(final_url)

    # extracts JSON from API call
    json_object = req.json()

    # prints json_object for testing purposes
    # print(json_object)

    # returns a JSON object for parsing
    return json_object


def parse_distance(jsons, origins, destinations):
    # Instantiates empty dictionary
    dictionary = {}
    # Iterate through each origin and destination
    for origin in origins:
        i = 0
        distances = []
        durations = []
        for destination in destinations:
            j = 0
            # Extracts distance and durations from json
            distance = jsons["rows"][i]["elements"][j]["distance"]["value"]
            duration = jsons["rows"][i]["elements"][j]["duration"]["value"]
            distances.append(distance)
            durations.append(duration)
            j += 1
        # Assigns the duration and distance list to the dictionary
        dictionary[origin] = {"distance": distances, "duration": durations}
        i += 1
    return dictionary


# TODO: Looking to average the distances of all information of latitude
# and longitude
def average_distances():
    pass


# TODO: Save out info from call_distance_api (Need to do in batches)
def save_info(API_KEY):
    origins = './geocoded/filtered.json'
    # TODO: We need to do this in batcnes and call the distance API
    destinations = ''
    # Utilize the API key here
    # for future testing: create two json files with an array of tuples for the origin and destination lat/long points
    # call_distance_api(
    #     "test_origin.json",
    #     "test_dest.json",
    #     API_KEY, 2020, 11, 3, 15)


# Scrape information from facilities_geocoded.csv
def scrape_facilities():
    df = pd.read_csv('./hh_resources/facilities_geocoded.csv')

    # Get each facility and put it in different destination files
    facility_dict = dict()
    for _, row in df.iterrows():
        if row['treatment_type']  not in facility_dict:
            facility_dict[row['treatment_type']] = []
        facility_dict[row['treatment_type']].append([row['latitude'], row['longitude']])

    # Iterate through each treatment type and put it into
    # its own json file
    for treatment_type, points in facility_dict.items():
        with open('./facilities/' + treatment_type + ".json", 'w') as f:
            json.dump(points, f)

def main():
    # API key for testing
    API_KEY = "AIzaSyBw7GB7DTvcrp0zprjarUvCuSij_gdcnBw"
    scrape_facilities()
    # test points using known addresses
    # # 471 Chestnut St, Springfield, MA 01107: 42.114440,-72.597300
    #
    # # 306 Race St, Holyoke, MA 01040: 42.200460,-72.607480
    #
    # # 141 East Main Street	Chicopee, MA 01020: 42.158780,-72.581460

    # for future testing: create two json files with an array of tuples for the origin and destination lat/long points
    # call_distance_api(
    #     "test_origin.json",
    #     "test_dest.json",
    #     API_KEY, 2020, 11, 3, 15)


if __name__ == "__main__":
    main()
