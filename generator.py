import random as rd
import math
import string

def euclidean(point1, point2):
    # Compute Euclidean distance between two points
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

# Set grid dimensions
grid_x = 1000
grid_y = 1000

# Set instance characteristics
number_stages = 6
number_locations = 10
number_customers = int(len(string.ascii_uppercase)/2)

# Create useful strings
str_locations = ', '.join([str(i) for i in range(1, number_locations + 1)])
str_customers = ', '.join(string.ascii_uppercase[:int(len(string.ascii_uppercase)/2)])

# Create random positions for locations
map_locations = {}
for location in range(0, number_locations):
    x = rd.randint(0, grid_x)
    y = rd.randint(0, grid_y)
    map_locations[location] = (x, y)

# Create random positions for customers
map_customers = {}
for customer in range(0, number_customers):
    x = rd.randint(0, grid_x)
    y = rd.randint(0, grid_y)
    map_customers[customer] = (x, y)

# Compute distances between customers and locations
distances = {}
for customer in range(0, number_customers):
    distances[customer] = {}
    for location in range(0, number_locations):
        distances[customer][location] = euclidean(map_customers[customer], map_locations[location])

# Compute rankings over locations based on distance
preferences = {}
for customer in range(0, number_customers):
    preferences[customer] = []
    for location, _ in sorted(distances[customer].items(), key = lambda x: x[1]):
        preferences[customer].append(str(location + 1))

# Create metadata.txt
with open('instances/random/metadata.txt', 'w') as output:
    output.write('{}\n'.format(number_stages))
    output.write('{}\n'.format(str_locations))
    output.write('{}\n'.format(str_customers))

# Create locations.csv
with open('instances/random/locations.csv', 'w') as output:
    output.write('id,m\n')
    for location in range(1, number_locations + 1):
        output.write('{},{}\n'.format(location, rd.randint(1,10)))

# Create revenues.csv
with open('instances/random/revenues.csv', 'w') as output:
    output.write('id,{}\n'.format(str_locations.replace(' ', '')))
    for customer in range(0, number_customers):
        output.write('{},{}\n'.format(string.ascii_uppercase[customer], ','.join([str(rd.randint(5,20)) for _ in range(0, number_locations)])))

# Create customers.csv
with open('instances/random/customers.csv', 'w') as output:
    output.write('id,{}\n'.format(str_locations.replace(' ', '')))
    for customer in range(0, number_customers):
        output.write('{},{}\n'.format(string.ascii_uppercase[customer], ','.join(preferences[customer])))

print('Random instance generated and exported to instances/random')