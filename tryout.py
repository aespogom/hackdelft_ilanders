from itertools import permutations
for x in range(1, 3):
    for perm in permutations(range(1, 4), x):
        route =  [0] + list(perm) + [0]
        print(route)



