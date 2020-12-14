import csv

from pathlib import Path
from geopy.geocoders import Nominatim

def main():

    # Utilize the geocoder to grab hospital geocode information
    geolocator = Nominatim(user_agent="DSV-WAV")
    # For logging purposes
    num = {"x": 0}

    # Add the hospital name and address. Don't need the names, but it's
    # visually clear.
    hospital_list = [
        ["Baystate Medical Center Springfield", "759 Chestnut St, Springfield, MA 01199"],
        ["Noble Hospital Westfield", "115 W Silver Street Westfield"],
        ["Baystate Wing Hospital -Palmer Medical Center", "40 Wright St, Palmer, MA 01069"],
        ["Baystate Mary Lane Outpatient Center: Emergency Room Ware", "85 South St, Ware, MA 01082"],
        ["Mercy Medical Center Springfield", "271 Carew St, Springfield, MA 01104"],
        ["Cooley Dickinson Hospital Northampton", "30 Locust St, Northampton, MA 01060"],
        ["Holyoke Medical Center Holyoke", "575 Beech St, Holyoke, MA 01040"],
        ["Baystate Franklin Medical Center Greenfield", "164 High St, Greenfield, MA 01301"],
        ["Berkshire Health Systems", "11 Quarry Hill Rd, Lee, MA 01238"],
        ["Athol Hospital", "2033 Main St, Athol, MA 01331"]
    ]

    with open("hospitals.csv",  'w', newline='') as f:
        writer = csv.writer(f)
        # Create a header for address, lat, long
        writer.writerow(["address", "latitude", "longitude"])
        for hospital in hospital_list:
            location = geolocator.geocode(hospital[0])
            if location is None:
                location = geolocator.geocode(hospital[1])
            print(location)
            if location is not None:
                writer.writerow([location.address, location.latitude, location.longitude])

if __name__ == "__main__":
    main()
