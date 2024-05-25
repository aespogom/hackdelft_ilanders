from utils import final_all_routes, get_distance, read_file, read_file_directions

# Example usage
api_key_file = 'secret.txt'  # Replace with your actual file path
api_key = read_file(api_key_file)

direction_list=read_file_directions("input_directions.txt")
matrix_distances_walk = []
matrix_distances_bike = []
matrix_distances_car = []
for x_axis, origin in enumerate(direction_list):
    matrix_distances_walk.append([])
    matrix_distances_bike.append([])
    matrix_distances_car.append([])
    for y_axis, destination in enumerate(direction_list):
        distance = get_distance(api_key, origin, destination, "walking")
        matrix_distances_walk[x_axis].append(distance)
        distance = get_distance(api_key, origin, destination, "bicycling")
        matrix_distances_bike[x_axis].append(distance)
        distance = get_distance(api_key, origin, destination, "driving")
        matrix_distances_car[x_axis].append(distance)

routes, distances = final_all_routes(matrix_distances_walk,
                                     matrix_distances_bike,
                                     matrix_distances_car)
print(routes)

# Comprobar todos los delivery points estan incluidos
# wanrning 

