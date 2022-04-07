import matplotlib.pyplot as plt
import argparse as ag
import instance as it
import backward as bd
import ast
import os

# Parse arguments using argparse
parser = ag.ArgumentParser(description = 'Draw graph with varying values of the number of samples for some instance')
parser.add_argument('folder', type = str, help = 'Path to the folder with instance files')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples (0 means full enumeration)', default = 0)
parser.add_argument('-d', '--decay', type = int, help = 'Set rationality decay parameter (1 means fully rational)', default = 1)
arguments = parser.parse_args()

# Create problem object with arguments
problem = it.Instance(arguments.folder, arguments.samples, arguments.decay)

# Create reference solver and run it
reference = bd.Backward(problem)
reference.run_solver()

# Decide variation of the sample values
if 'medium' in arguments.folder:
    # For medium instance
    sample_values = list(range(1,16))
else:
    # For large instance
    sample_values = [10,20,30,40,50,60,70,80,90,100,120,140,160,180,200]


# Create dictionary to store error
error_J = {}

# For each value of s, each time period k, and each state x...
# There are either 100 runs (medium instance) or 10 runs (large instance)...
# Store the list to later compute the average error
for s in sample_values:
    error_J[s] = {}
    for k in problem.K:
        error_J[s][k] = {}
        for x in problem.X:
            error_J[s][k][x] = []

# Loop over values of parameter s
for s in sample_values:

    # Retrieve policies in the policy folder with current s (and global d)
    policies = []
    pattern = '{}_{}_{}_{}'.format('backward', problem.name, s, arguments.decay)
    print('Looking for stored policies with pattern {}'.format(pattern))

    # Retrieve the dictionary with the policy from the file using ast package
    for file in os.listdir('policies'):
        if pattern in file:
            print('\tFound policy {}'.format(file))
            with open('policies/{}'.format(file)) as output:
                content = output.read()
            policy = ast.literal_eval(content)
            policies.append(policy)

    # Loop over retrieved policies in the last step
    for identifier, policy in enumerate(policies):

        print('Evaluating policy #{}'.format(identifier))

        # Compute the J_k(x) value according to policy
        # Using the reference solver, "perfect" information
        evaluated_J = reference.evaluate_policy(policy)

        for k in problem.K:
            for x in problem.X:
                # Compute the error of the policy based on the reference
                error = evaluated_J[k][x] - reference.J(k, x)
                error_J[s][k][x].append(error)

# Report only for k = 0 and x = 0
k = 0
x = '0'

# Compute average over 100 runs (medium instance) or 10 runs (large instance)
data = []
for s in sample_values:
    if len(error_J[s][k][x]) > 0:
        avg = sum(error_J[s][k][x]) / len(error_J[s][k][x])
        data.append(avg)

# Plot averge error of J_0(0) values
plt.plot(sample_values, data, '-x')
# Set other graph settings
plt.ylabel('Average sub-optimality of the J_0(0) value'.format(k, k))
plt.xlabel('Number of samples s')
plt.savefig('graphs/samples_{}_{}_{}.png'.format(problem.name, k, x))
plt.close()

print('Exported sample graph to {}'.format('graphs/samples_{}_{}_{}.png'.format(problem.name, k, x)))