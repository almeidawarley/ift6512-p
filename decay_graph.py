import matplotlib.pyplot as plt
import argparse as ag
import instance as it
import backward as bd

# Parse arguments using argparse
parser = ag.ArgumentParser(description = 'Draw graph with varying values of the rationality decay parameter for some instance')
parser.add_argument('folder', type = str, help = 'Path to the folder with instance files')
parser.add_argument('max_decay', type = int, help = 'Maximum value for the rationality decay parameter')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples (0 means full enumeration)', default = 0)
arguments = parser.parse_args()

# Create problem object with d = 1
problem = it.Instance(arguments.folder, arguments.samples, 1)

# Create list of values of parameter d
ds = [1, 1.2, 1.4, 1.6, 1.8] + list(range(2, arguments.max_decay + 1))

# Create dictionary to store J_0(x) values
# The list has values for d = 1, ..., max_decay
bJs = {}
for x in problem.X:
    bJs[x] = []

# Loop over values of parameter d
for d in ds:

    # Set parameter d in the instance
    problem.d = d
    # Run the backward solver
    solver = bd.Backward(problem)
    solver.run_solver()

    # Store the J_0(x) values
    k = 0
    for x in problem.X:
        bJs[x].append(solver.J(k, x))

# Set colors for up to 11 states
color = {
    '0': 'red',
    '1': 'blue',
    '2': 'yellow',
    '3': 'green',
    '4': 'orange',
    '5': 'darkviolet',
    '6': 'teal',
    '7': 'gray',
    '8': 'chocolate',
    '9': 'magenta',
    '10': 'black'
}

# Plot J_0(x) values for each state x
for x in problem.X:
    plt.plot(ds, bJs[x], '-x', label = 'J_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)

# Set other graph settings
plt.xlabel('Rationality decay parameter d')
plt.ylabel('Optimal cost-to-go function J_0(x)')
plt.legend(loc = 'upper right')
plt.savefig('graphs/decay_{}.png'.format(problem.name))
plt.close()

print('Exported decay graph to {}'.format('graphs/decay_{}.png'.format(problem.name)))