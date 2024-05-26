from datetime import datetime
import googlemaps
from itertools import permutations
import Constants
import variables 
import numpy as np


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def read_file_directions(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Remove the newline characters from each line
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def get_distance(api_key, origin, destination, mode):
    # Initialize the client with the API key
    gmaps = googlemaps.Client(key=api_key)
    
    # Request directions via walking
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode=mode,
                                         departure_time=datetime.now())
    
    # Extract the distance
    if directions_result:
        distance = directions_result[0]['legs'][0]['distance']['text']
        # duration = directions_result[0]['legs'][0]['duration']['text']
        if distance.endswith(" m"):
            convert_number = distance.split(" m")
            convert_number = convert_number[0].replace(',', '')
            return float(convert_number)/1000
        else:
            convert_number = distance.split(" km")
            convert_number = convert_number[0].replace(',', '')
            return float(convert_number)
    else:
        return None
    
def final_all_routes(distances_walking,
                     distances_bike,
                     distances_car):
    # Remove the first row using slicing
    inner_distances = distances_walking[1:]
    
    # Remove the first column from each remaining row using a list comprehension
    inner_distances = [row[1:] for row in inner_distances]
    num_nodes = len(inner_distances)
    all_routes = []
    all_distances = []
    all_time = []
    for n_stops in range(1, num_nodes):   
        for perm in permutations(range(1, num_nodes+1), n_stops):
            route =  [0] + list(perm) + [0]
            distance_point_walk = 0
            time_point_walk = 0
            distance_point_bike = 0
            time_point_bike = 0
            distance_point_car = 0
            time_point_car = 0
            for idx, point in enumerate(route[:-1]):
                if variables.is_sunny:
                    if time_point_walk <= Constants.t_working and len(route) <= variables.n_magazines_walk + 2:
                        distance_point_walk += distances_walking[point][route[idx+1]]
                        time_point_walk += distances_walking[point][route[idx+1]]/Constants.v_walk + Constants.t_stop
                        if distances_walking[point][route[idx+1]]/Constants.v_walk  > Constants.t_max_walking:
                            time_point_walk += Constants.t_stop
                    else:
                        distance_point_walk = np.nan
                        time_point_walk = np.nan
                    
                    if time_point_bike <= Constants.t_working and distance_point_bike <= Constants.d_max_ebike and len(route) <= variables.n_magazines_bike + 2:
                        distance_point_bike += distances_bike[point][route[idx+1]]
                        time_point_bike += distances_bike[point][route[idx+1]]/Constants.v_ebike + Constants.t_stop
                        if distances_bike[point][route[idx+1]]/Constants.v_ebike  > Constants.t_max_bike:
                            time_point_bike += Constants.t_stop
                    else:
                        distance_point_bike = np.nan
                        time_point_bike = np.nan
                        
                    if time_point_car <= Constants.t_working:
                        distance_point_car += distances_car[point][route[idx+1]]
                        time_point_car += distances_car[point][route[idx+1]]/Constants.v_car + Constants.t_stop
                        if distances_car[point][route[idx+1]]/Constants.v_car  > Constants.t_max_car:
                            time_point_car += Constants.t_stop
                    else:
                        distance_point_car = np.nan
                        time_point_car = np.nan
                else:
                    if time_point_car <= Constants.t_working:
                        distance_point_car += distances_car[point][route[idx+1]]
                        time_point_car += distances_car[point][route[idx+1]]/Constants.v_car + Constants.t_stop
                        if distances_car[point][route[idx+1]]/Constants.v_car  > Constants.t_max_car:
                            time_point_car += Constants.t_stop
                    else:
                        distance_point_car = np.nan
                        time_point_car = np.nan

            all_routes.append(route)
            all_distances.append([distance_point_walk, distance_point_bike, distance_point_car])
            all_time.append([time_point_walk, time_point_bike, time_point_car])

    return all_routes, all_distances, all_time

def eliminate_routes(all_routes, all_distances, all_times):

    all_routes = np.array(all_routes, dtype=object)
    all_distances = np.array(all_distances, dtype=object)
    all_times = np.array(all_times, dtype=object)
    
    # Convert 'nan' strings to np.nan in all_distances
    all_distances = np.where(all_distances == 'nan', np.nan, all_distances).astype(float)
    
    # Find rows where all elements in all_distances are NaN
    rows_with_all_nan = np.all(np.isnan(all_distances), axis=1)
    
    # Use boolean indexing to filter out rows with all NaNs
    all_possible_routes = all_routes[~rows_with_all_nan]
    all_possible_distances = all_distances[~rows_with_all_nan]
    all_possible_times = all_times[~rows_with_all_nan]

    # Find rows where all elements are NaN
    #rows_with_all_nan = np.all(np.isnan(all_distances), axis=1)

    # Extract the indices of these rows
    #remove_route = np.argwhere(rows_with_all_nan).flatten()

    #all_possible_routes = all_routes.pop(int(remove_route))
    #all_possible_distances = all_distances.pop(remove_route)
    #all_possible_times = all_times.pop(remove_route)

    return all_possible_routes, all_possible_distances, all_possible_times

def check_locations(all_possible_routes, address):
    for n_address in range(0, len(address)):
        if not any(n_address in route for route in all_possible_routes):
            print('Address ' + address[n_address]+ ' is not reachable')




    
