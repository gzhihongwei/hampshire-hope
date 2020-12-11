import json


# Load the geojson file of all MA town boundaries
with open('ma_towns.json', 'r') as f:
    ma_towns = json.load(f)
    
# All Hampshire County towns & cities
hampshire_cities = [
    'AMHERST', 'BELCHERTOWN', 'CHESTERFIELD', 'CUMMINGTON', 'EASTHAMPTON',
    'GOSHEN', 'GRANBY', 'HADLEY', 'HATFIELD', 'HUNTINGTON', 'MIDDLEFIELD',
    'NORTHAMPTON', 'PELHAM', 'PLAINFIELD', 'SOUTH HADLEY', 'SOUTHAMPTON',
    'WARE', 'WESTHAMPTON', 'WILLIAMSBURG', 'WORTHINGTON'
]  

# All Hampden County towns & cities that Hampshire Hope operates in
hampden_cities = [
    "CHICOPEE", "EAST LONGMEADOW", "HAMPDEN", "HOLYOKE", 
    "LONGMEADOW", "LUDLOW", "PALMER", "WESTFIELD", 
    "WEST SPRINGFIELD", "WILBRAHAM"
]

# Filters the towns to the towns of interest
towns_of_interest = list(filter(lambda town: town['properties']['TOWN'] in hampshire_cities + hampden_cities, ma_towns['features']))

# Reassign the relevant town boundaries for geojson
ma_towns['features'] = towns_of_interest

# Redump modified geojson to a new json file
with open('toi.json', 'w') as f:
    json.dump(ma_towns, f)