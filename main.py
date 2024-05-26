from linear_prog import optimize
from utils import final_all_routes, get_distance, read_file, read_file_directions
import pandas as pd

# Example usage
api_key_file = 'secret.txt'  # Replace with your actual file path
API_KEY = read_file(api_key_file)

direction_list=read_file_directions("input_directions.txt")
matrix_distances_walk = []
matrix_distances_bike = []
matrix_distances_car = []
for x_axis, origin in enumerate(direction_list[0:4]):
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

# Comprobar todos los delivery points estan incluidos
# wanrning 

inputs = pd.read_csv("inputs.csv")
optimize(routes, distances, times, inputs)

def final_result():
    routes = [
        ("walking", [
            "Markt 87, 2611 GS Delft",
            "Olof Palmestraat 1, 2616 LN Delft",
            "Troelstralaan 71, 2624 ET Delft"
        ]),
        ("driving", [
            "Schieweg 15L, 2627 AN Delft",
            "Westeinde 2A, 2275 AD Voorburg",
            "Troelstralaan 71, 2624 ET Delft"
        ])
    ]
    return routes