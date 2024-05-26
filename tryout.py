import numpy as np
from utils import final_all_routes, get_distance, read_file, read_file_directions, eliminate_routes, check_locations

address=read_file_directions("input_directions.txt")
all_possible_routes = [[0, 1, 0], [0, 3, 4, 5, 6, 7, 8, 9, 0]]


for n_address in range(0, len(address)):
    if not any(n_address in route for route in all_possible_routes):
        print('Address ' + address[n_address]+ ' is not reachable')




