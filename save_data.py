import datetime
import json
import os
import pickle
import pandas as pd
from pprint import pprint

from query_google import call_distance_api, parse_distance


OPTIMAL_BATCH_SIZES = {
    "Acute Treatment and Stabilization Services -Youth": 0,
    "Acute Treatment Services-Adults": 0,
    "Clinical Support Service": 0,
    "Co-occurring Enhanced Residential Recovery Service": 0,
    "Intervention and Family Support Programs": 0,
    "Jail Diversion Residential and Case Management": 0,
    "Mass Opiate Abuse Prevention Collaboratives": 0,
    "Office-based Opiod Treatment (Buprenorphine and Vivitrol Treatment)": 14,
    "Opiod Treatment Programs (Methadone and Buprenorphine Treatment)": 0,
    "Outpatient Services": 13,
    "Overdose Prevention and Syringe Access Programs": 0,
    "Recovery High School": 0,
    "Recovery Support Services and Centers": 0,
    "Residential Recovery Programs": 8,
    "Substance Use Prevention Programs": 0,
    "Supportive Housing": 0,
    "Transitional Support Service": 0
}


def create_batches(inputs, batch_size):
    """
    Creates batches from `inputs`
    
    Parameters
    ----------
    - `inputs: List`
        List to create batches from
    - `batch_size: int`
        Batch size
        
    Returns
    -------
    `List`
        Returns a list of lists, each of length `batch_size`
    """
    
    return [inputs[i:i + batch_size] for i in range(0, len(inputs), batch_size)]


def treatment_type_metrics(origins, treatment_type, arrival_hour, batch_size = 0):
    """
    Returns a dictionary which maps `origins` to a dictionary of the durations and 
    times to each treatment center of type `treatment_type`.
    
    Parameters
    ----------
    - `origins: List[Tuple[int]]`
        List of latitude, longitude points
    - `treatment_type: str`
        String indicating which treatment type to look for
    - `arrival_hour: int`
        Int indicating what hour to arrive
    - `batch_size: int`
        Int indicating batch sizes for destinations. Default 0 means no batching needed.
        
    Returns
    -------
    `dict`
        Returns a dictionary that maps `origins` to a dictionary of the durations and 
        times to each treatment center of type `treatment_type`.
    """
    
    # API key for testing
    API_KEY = "AIzaSyC2CFyh-OE27egOLMYdWyXoglF-aA4LET8"
    
    # Path to destinations folder
    destinations_path = os.path.join("facilities", treatment_type + ".json")
    
    # Loads the appropriate json
    with open(destinations_path, "r") as f:
        destinations = json.load(f)
    
    # Creates batches if necessary
    destinations = create_batches(destinations, batch_size) if batch_size > 0 else [destinations]
    # Current time
    now = datetime.datetime.now()
    # List of the different destination batches
    batches = list()
    
    # Iterates over each destination batch
    for i, destination_batch in enumerate(destinations):
        
        # Creates appropriate batches for origins
        origin_batches = create_batches(origins, 20 - len(destination_batch))
        # Stores metrics to destinations in current batch
        batch_map = dict()
        
        # Iterates over all origins
        for j, origin_batch in enumerate(origin_batches):
            
            # Gets the query result from Google's Distance Matrix API
            query_result = call_distance_api(origin_batch, destination_batch, API_KEY, now.year, now.month, now.day, arrival_hour)
            # Parsed query result
            parsed_result = parse_distance(query_result, origin_batch)
            # Update batch_map
            batch_map.update(parsed_result)
            
            # Print every 200 queries
            if j % 200 == 0:
                print(f"Destination batch {i + 1}, origin batch {j + 1}")
                
        # Add batch_map to batches
        batches.append(batch_map)
    
    # Final map
    mapping = dict()
    
    # Iterates over all points
    for point in batches[0].keys():
        
        # Final distance and durations lists
        distances = list()
        durations = list()
        
        # Creates the final distance and durations lists
        for batch in batches:
            distances.extend(batch[point]["distance"])
            durations.extend(batch[point]["duration"])
            
        # Updates map
        mapping[point] = {"distance": distances, "duration": durations}
    
    return mapping
        

def main():
    
    with open(os.path.join("geocoded", "filtered.json"), "r") as f:
        origins = json.load(f)
        
    # origins = origins[:30]
    
    treatment_types = ["Residential Recovery Programs"]
    
    for treatment_type in treatment_types:
        metrics = treatment_type_metrics(origins, treatment_type, 8, OPTIMAL_BATCH_SIZES[treatment_type])
        
        path = os.path.join("google_data", treatment_type + ".pkl")
        
        with open(path, "wb") as f:
            pickle.dump(metrics, f)
    
    
if __name__ == "__main__":
    main()