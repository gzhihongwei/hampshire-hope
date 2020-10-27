import requests
import json
import datetime
from datetime import timezone

# beginning of every API call to the Google Matrix API for json objects
URL_DIST = "https://maps.googleapis.com/maps/api/distancematrix/json?"

# Documenation for Google Distance Matrix: https://developers.google.com/maps/documentation/distance-matrix/overview?authuser=2#DistanceMatrixRequests
# creates and calls a url for the Google Distance Matrix; returns the json object produced from the API call
# things to keep in mind: Google only has information for the next few weeks from the current date
# 
def call_distance_api(origins, destinations, key, arrival_year, arrival_month, arrival_hour):
    str_of_origin = ""
    str_of_dest = ""
    # creates a string of all the lats and longs of each origin point in the array of origins in the
    # form of lat,long|lat,long|...
    for origin in origins:
        str_of_origin += str(origin[0]) + "," + str(origin[1]) + "|"
    # creates a string of all the lats and longs of each destination point in the array of destinations in the
    # form of lat,long|lat,long|...
    for dest in destinations:
        str_of_dest += str(dest[0]) + "," + str(dest[1]) + "|"

    # removes the last | from both strings
    str_of_origin = str_of_origin[:-1]
    str_of_dest = str_of_dest[:-1]

    # converts given year, month, hour to UTC time; assumes day as the 1st of the given month and minute and second at 0
    time = datetime.datetime(year=arrival_year, month=arrival_month, day=1, hour=arrival_hour, minute=0, second=0)
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
    json_file = req.json()

    # prints json_file for testing purposes
    print(json_file)

    # returns JSON file for parsing
    return json_file


def main():
    #API key for testing
    API_KEY = "AIzaSyBw7GB7DTvcrp0zprjarUvCuSij_gdcnBw"

    # test using source points
    call_distance_api([[42.1833902, -73.0140060055118], [42.04674958740158, -72.2904562047244], [42.3438605, -72.3052605480315]],
                    [[42.34770698740157, -72.41447856614172],[42.1666842677153, -72.37188009291339]],
                    API_KEY, 2020, 11, 5)

    # test points using known addresses
    # 471 Chestnut St, Springfield, MA 01107: 42.114440,-72.597300

    # 306 Race St, Holyoke, MA 01040: 42.200460,-72.607480

    # 141 East Main Street	Chicopee, MA 01020: 42.158780,-72.581460

    call_distance_api(
        [[42.114440, -72.597300]],
        [[42.200460, -72.607480], [42.158780, -72.581460]],
        API_KEY, 2020, 11, 5)

    call_distance_api(
        [[42.114440, -72.597300]],
        [[42.200460, -72.607480], [42.158780, -72.581460]],
        API_KEY, 2020, 11, 15)


if __name__ == "__main__":
    main()