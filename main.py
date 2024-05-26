from linear_prog import optimize
from utils import final_all_routes, get_distance, read_file, read_file_directions, eliminate_routes, check_locations
import pandas as pd
import csv
import os
import pickle

# Example usage
api_key_file = 'secret.txt'  # Replace with your actual file path
API_KEY = read_file(api_key_file)

direction_list=read_file_directions("input_directions.txt")
if not os.path.exists("possible_routes.csv"):
    matrix_distances_walk = []
    matrix_distances_bike = []
    matrix_distances_car = []
    for x_axis, origin in enumerate(direction_list):
        matrix_distances_walk.append([])
        matrix_distances_bike.append([])
        matrix_distances_car.append([])
        for y_axis, destination in enumerate(direction_list):
            distance = get_distance(API_KEY, origin, destination, "walking")
            matrix_distances_walk[x_axis].append(distance)
            distance = get_distance(API_KEY, origin, destination, "bicycling")
            matrix_distances_bike[x_axis].append(distance)
            distance = get_distance(API_KEY, origin, destination, "driving")
            matrix_distances_car[x_axis].append(distance)

    routes, distances, times = final_all_routes(matrix_distances_walk,
                                        matrix_distances_bike,
                                        matrix_distances_car)

    possible_routes, possible_distances, possible_times = eliminate_routes(routes,
                                                                        distances,
                                                                        times)
    # Save to a CSV file
    with open('possible_routes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(possible_routes)
    file.close()
    with open('possible_distances.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(possible_distances)
    file.close()
    with open('possible_times.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(possible_times)
    file.close()
else:
    # Read from a CSV file
    with open('possible_routes.csv', 'r') as file:
        reader = csv.reader(file)
        possible_routes = [list(map(int, row)) for row in reader]
    file.close()
    with open('possible_distances.csv', 'r') as file:
        reader = csv.reader(file)
        possible_distances = [list(map(float, row)) for row in reader]
    file.close()
    with open('possible_times.csv', 'r') as file:
        reader = csv.reader(file)
        possible_times = [list(map(float, row)) for row in reader]
    file.close()

# Comprobar todos los delivery points estan incluidos
# wanrning 
check_locations(possible_routes, direction_list)


inputs = pd.read_csv("inputs.csv")
result_obj, result_vars = optimize(possible_routes, possible_distances, possible_times, inputs)


RESULT_VARS = result_vars
POSSIBLE_ROUTES = possible_routes
DIRECCTION_LIST = direction_list

def final_result():
    routes = []
    for route in RESULT_VARS:
        mode = route.split("_")[-1]
        index_route = int(route.split("_")[1])
        if mode.endswith("ecar"):
            travelMode = "driving"
        elif mode == "bike":
            travelMode = "bicycling"
        else:
            travelMode=mode
        waypoints = [DIRECCTION_LIST[i] for i in POSSIBLE_ROUTES[index_route]]
        routes.append(
            (travelMode, waypoints)
        )
    return routes
