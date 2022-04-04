import random as rd
import uuid
import math
import string

def euclidean(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

grid_x = 1000
grid_y = 1000

name = str(uuid.uuid4())[:8]

number_stages = 12
number_locations = 10
number_customers = len(string.ascii_uppercase)
number_samples = 100
rational_coef = 10

map_locations = {}
map_customers = {}

str_locations = ', '.join([str(i) for i in range(1, number_locations + 1)])
str_customers = ', '.join(string.ascii_uppercase)

for location in range(0, number_locations):
    x = rd.randint(0, grid_x)
    y = rd.randint(0, grid_y)
    map_locations[location] = (x, y)

for customer in range(0, number_customers):
    x = rd.randint(0, grid_x)
    y = rd.randint(0, grid_y)
    map_customers[customer] = (x, y)

distances = {}
for customer in range(0, number_customers):
    distances[customer] = {}
    for location in range(0, number_locations):
        distances[customer][location] = euclidean(map_customers[customer], map_locations[location])

preferences = {}
for customer in range(0, number_customers):
    preferences[customer] = []
    for location, _ in sorted(distances[customer].items(), key = lambda x: x[1]):
        preferences[customer].append(str(location + 1))

print(preferences)

# Create metadata.txt
with open('instances/random/metadata.txt', 'w') as output:
    output.write('{}\n'.format(number_stages))
    output.write('{}\n'.format(str_locations))
    output.write('{}\n'.format(str_customers))
    output.write('{}\n'.format(number_samples))
    output.write('{}'.format(rational_coef))

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