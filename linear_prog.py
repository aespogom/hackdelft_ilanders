import pulp
import Constants
import variables
from pulp import PULP_CBC_CMD, COIN_CMD
import numpy as np

# Function to find indexes of lists containing a specific number
def find_indexes(matrix, number):
    return [index for index, row in enumerate(matrix) if number in row]

def add_constrains(lp_problem, routes_matrix, variables, inputs):
   # Initialize an empty set to store unique numbers
    unique_delivery_points = set()

    # Iterate through each sublist and add the numbers to the set
    for sublist in routes_matrix:
        unique_delivery_points.update(sublist)
    unique_delivery_points.remove(0)
    for delivery_point in unique_delivery_points:
        indexes_route_delivery_point = find_indexes(routes_matrix, delivery_point)
        var_names_constrain = []
        for index, name in enumerate(variables):
            if index in indexes_route_delivery_point:
                var_names_constrain.append(variables[name])
        # Pasar una vez por cada waypoint
        if inputs["num_magazines"].iloc[0]>=len(unique_delivery_points):
            lp_problem += pulp.lpSum(var_names_constrain) == 1, f"Constraint {delivery_point}"
        else:
            lp_problem += pulp.lpSum(var_names_constrain) <= 1, f"Constraint {delivery_point}"

    car_varibles = [variables[s] for s in list(variables.keys()) if s.endswith("_car")]
    if len(car_varibles):
        lp_problem += pulp.lpSum(car_varibles) <= inputs["num_cars"].iloc[0], f"Constraint num car"
    ecar_varibles = [variables[s] for s in list(variables.keys()) if s.endswith("_ecar")]
    if len(ecar_varibles):
        lp_problem += pulp.lpSum(ecar_varibles) <= inputs["num_ecars"].iloc[0], f"Constraint num ecar"
    bike_varibles = [variables[s] for s in list(variables.keys()) if s.endswith("_bike")]
    if len(bike_varibles):
        lp_problem += pulp.lpSum(bike_varibles) <= inputs["num_bikes"].iloc[0], f"Constraint num bikes"
    walk_varibles = [variables[s] for s in list(variables.keys()) if s.endswith("_walking")]
    if len(walk_varibles):
        lp_problem += pulp.lpSum(walk_varibles) <= inputs["num_walk"].iloc[0], f"Constraint num people"



    return lp_problem

def optimize(routes_matrix, distances_matrix, temp_matrix, inputs):
    variable_names = []
    # Numero de veces que pasamos por la ruta X por cada metodo de travel
    for index, _ in enumerate(routes_matrix):
        tmp_var_names = []
        if not np.isnan(distances_matrix[index][0]):
            tmp_var_names.append("x_"+str(index)+"_walking")
        if not np.isnan(distances_matrix[index][1]):
            tmp_var_names.append("x_"+str(index)+"_bike")
        if not  np.isnan(distances_matrix[index][2]):
            tmp_var_names.append("x_"+str(index)+"_car")
            tmp_var_names.append("x_"+str(index)+"_ecar")
        variable_names.append(tmp_var_names)

    # Create the linear programming problem
    lp_problem = pulp.LpProblem("MinCosts", pulp.LpMinimize)

    # Create decision variables dynamically
    # Flatten the list of lists
    flat_variable_names = [name for sublist in variable_names for name in sublist]

    # Create the dictionary of variables
    variables = {name: pulp.LpVariable(name, lowBound=0, cat='Binary') for name in flat_variable_names}

    # Define the objective function dynamically
    # Walking
    coefficients_list = []
    for name_var in flat_variable_names:
        index = int(name_var.split("_")[1])
        mode = name_var.split("_")[2]
        if mode =="walking":
            coeff = Constants.wage*temp_matrix[index][0]
        elif mode =="car":
            coeff = Constants.wage*temp_matrix[index][2] + Constants.price_gasoline*distances_matrix[index][2]
        elif mode =="ecar":
            coeff= Constants.wage*temp_matrix[index][2] + Constants.price_Ecar*distances_matrix[index][2]
        elif mode =="bike":
            coeff = Constants.wage*temp_matrix[index][1] + Constants.price_ebike*distances_matrix[index][1]
        coefficients_list.append(coeff)
    lp_problem += pulp.lpSum([coefficients_list[index] * variables[name] for index, name in enumerate(flat_variable_names)]), "Objective Function"

    # Define the constraints dynamically
    lp_problem = add_constrains(lp_problem, routes_matrix=routes_matrix, variables=variables, inputs=inputs)

    # Solve the problem
    try:
        solver = COIN_CMD(msg=True, path="c:\\Users\\anaes\\anaconda3\\envs\\ilanders\\Lib\\site-packages\\pulp\\solverdir\\cbc\\win\\64\\cbc.exe")
        lp_problem.solve(solver)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Check and print the result
    print("Status:", pulp.LpStatus[lp_problem.status])
    print("Optimal value:", pulp.value(lp_problem.objective))
    final_variables = []
    for var in variables.values():
        if pulp.value(var)>0:
            final_variables.append(var.name)
    return pulp.value(lp_problem.objective), final_variables
