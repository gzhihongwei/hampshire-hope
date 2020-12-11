import csv
import requests
import json
import time


def load_array_of_route():
    """
          Makes a request to the PVTA bustracker website which contains an XML file with live updates for
          the bus schedule. Creates and loads this data into a json file.
    """
    url = 'http://bustracker.pvta.com/InfoPoint/rest/routedetails/getallroutedetails'

    # creating HTTP response object from given url
    req = requests.get(url)
    # saving the xml file into a JSON file
    with open('pvta_routes.json', 'wb') as f:
        f.write(req.content)


def parse_json_file(json_file, dict_of_routes):
    """
          Parses json_file for the bus's name, vehicle id, and the location fo the bus through longitude and latitude
          ---
          Parameters
          - json_file: json file that contains the information scraped from the bustracker XML file
          - dict_of_routes: where scraped information is stored (passing it in as a parameter allows us to keep
          updating the same dictionary in a loop)

    """
    with open(json_file) as json_file:
        arr_of_routes = json.load(json_file)
        for route in arr_of_routes:
            bus_name = route["RouteAbbreviation"]
            if len(route["Vehicles"]) > 0:
                vehicles = route["Vehicles"]
                for vehicle in vehicles:
                    if bus_name not in dict_of_routes.keys():
                             dict_of_routes[bus_name] = {}
                    vehicle_id = vehicle["VehicleId"]
                    if vehicle_id not in dict_of_routes[bus_name]:
                             dict_of_routes[bus_name][vehicle_id] = []
                    arr_of_info = []
                    arr_of_info.append(vehicle["Latitude"])
                    arr_of_info.append(vehicle["Longitude"])
                    dict_of_routes[bus_name][vehicle_id].append(arr_of_info)




def savetoCSV(dict_of_routes):
    """
              Stores information scraped from the bustracker XML in the dictionary into a CSV file for mapping
              ---
              Parameters
              - dict_of_routes: dictionary used to populate the CSV file

        """
    # specifying the fields for csv file
    fields = ['Bus Name', 'Vehicle ID', 'Latitude', 'Longitude']

    # writing to csv file
    with open("parse_routes.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()
        # parses through dictionary
        for bus_key, bus_value in dict_of_routes.items():
            for vehicle_key, vehicle_value in bus_value.items():
                for info in vehicle_value:
                    writer.writerow(
                        {'Bus Name': bus_key, 'Vehicle ID': vehicle_key, 'Latitude': info[0],
                         'Longitude': info[1]})


def main():
    # test
    dict_of_routes = {}
    count = 0
    while (count < 720):
        load_array_of_route()

        parse_json_file("pvta_routes.json", dict_of_routes)

        count += 1

        time.sleep(10)

    savetoCSV(dict_of_routes)


if __name__ == "__main__":
    # calling main function
    main()
