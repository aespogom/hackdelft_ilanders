from datetime import datetime
import googlemaps
from itertools import permutations


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
    for perm in permutations(range(1, num_nodes)):
        route =  [0] + list(perm) + [0]
        distance_point_walk = 0
        time_walk = 0
        distance_point_bike = 0
        time_bike = 0
        distance_point_car = 0
        time_car = 0
        for point in route[:-1]:
            distance_point_walk =+ distances_walking[point][route[point+1]]
            time_walk =+ SPEED_WALK*distances_walking[point][route[point+1]] + 1/6
            if SPEED_WALK*distances_walking[point][route[point+1]]  > 0.75:
                time_walk += 1/6
            distance_point_car =+ distances_car[point][route[point+1]]
            time_car =+ SPEED_CAR*distances_car[point][route[point+1]] + 1/6
            if SPEED_CAR*distances_car[point][route[point+1]]  > 2:
                time_car += 1/6
            distance_point_bike =+ distances_bike[point][route[point+1]]
            time_bike =+ SPEED_BIKE*distances_bike[point][route[point+1]] + 1/6
            if SPEED_BIKE*distances_bike[point][route[point+1]]  > 0.75:
                time_bike += 1/6

        all_routes.append(route)
        all_distances.append([distance_point_walk, distance_point_bike, distance_point_car])
    return all_routes, all_distances