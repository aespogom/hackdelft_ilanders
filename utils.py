from datetime import datetime
import googlemaps
from itertools import permutations
import Constants
import variables 


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
            return float(convert_number[0])/1000
        else:
            convert_number = distance.split(" km")
            return float(convert_number[0])
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
                    if time_point_walk <= Constants.t_working:
                        distance_point_walk =+ distances_walking[point][route[idx+1]]
                        time_point_walk =+ Constants.v_walk*distances_walking[point][route[idx+1]] + Constants.t_stop
                        if Constants.v_walk*distances_walking[point][route[idx+1]]  > Constants.t_max_walking:
                            time_point_walk += Constants.t_stop
                    else:
                        distance_point_walk = float("nan")
                        time_point_walk = float("nan")
                    
                    if time_point_bike <= Constants.t_working or distance_point_bike <= Constants.d_max_ebike:
                        distance_point_bike =+ distances_bike[point][route[idx+1]]
                        time_point_bike =+ Constants.v_ebike*distances_bike[point][route[idx+1]] + Constants.t_stop
                        if Constants.v_ebike*distances_bike[point][route[idx+1]]  > Constants.t_max_bike:
                            time_point_bike += Constants.t_stop
                    else:
                        distance_point_bike = float("nan")
                        time_point_bike = float("nan")
                        
                    if time_point_car <= Constants.t_working:
                        distance_point_car =+ distances_car[point][route[idx+1]]
                        time_point_car =+ Constants.v_car*distances_car[point][route[idx+1]] + Constants.t_stop
                        if Constants.v_car*distances_car[point][route[idx+1]]  > Constants.t_max_car:
                            time_point_car += Constants.t_stop
                    else:
                        distance_point_car = float("nan")
                        time_point_car = float("nan")
                else:
                    if time_point_car <= Constants.t_working:
                        distance_point_car =+ distances_car[point][route[idx+1]]
                        time_point_car =+ Constants.v_car*distances_car[point][route[idx+1]] + Constants.t_stop
                        if Constants.v_car*distances_car[point][route[idx+1]]  > Constants.t_max_car:
                            time_point_car += Constants.t_stop
                    else:
                        distance_point_car = float("nan")
                        time_point_car = float("nan")

            all_routes.append(route)
            all_distances.append([distance_point_walk, distance_point_bike, distance_point_car])
            all_time.append([time_point_walk, time_point_bike, time_point_car])

    return all_routes, all_distances, all_time

def check_locations(all_possible_routes, address):
    for n_address in range(0, len(address)):
        if not n_address in all_possible_routes:
            print('Address ' + address[n_address]+ ' is not reachable')




    
