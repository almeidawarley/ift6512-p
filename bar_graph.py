
import matplotlib.pyplot as plt
import numpy as np
import argparse as ag
import instance as it
import backward as bd
import ast
import os

# Parse arguments using argparse
parser = ag.ArgumentParser(description = 'Draw bar graph comparing the parametric policy with the backward policy for some instance')
parser.add_argument('folder', type = str, help = 'Path to the folder with instance files')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples (0 means full enumeration)', default = 0)
parser.add_argument('-d', '--decay', type = int, help = 'Set rationality decay parameter (1 means fully rational)', default = 1)
arguments = parser.parse_args()

# Create problem object with arguments
problem = it.Instance(arguments.folder, arguments.samples, arguments.decay)

# Create reference solver and run it
reference = bd.Backward(problem)
reference.run_solver()

# Retrieve parametric policy
policy = {}
pattern = '{}_{}_{}_{}'.format('parametric', problem.name, arguments.samples, arguments.decay)
print('Looking for stored policy with pattern {}'.format(pattern))
for file in os.listdir('policies'):
    if pattern in file:
        print('\tFound policy {}'.format(file))
        with open('policies/{}'.format(file)) as output:
            content = output.read()
        policy = ast.literal_eval(content)

# Create list to store optimal J_0(x) values (i.e., from backward policy)
optimal_J = []
# Create list to store sub-optimal J_0(x) values (i.e., from parametric policy)
suboptimal_J = []

print('Evaluating parametric policy')
# Compute the J_k(x) value according to policy
# Using the reference solver, "perfect" information
evaluated_J = reference.evaluate_policy(policy)
# Report only for k = 0
k = 0
for x in problem.X:
    # Compute the error of the policy based on the reference
    error = evaluated_J[k][x] - reference.J(k, x)
    optimal_J.append(reference.J(k, x))
    suboptimal_J.append(evaluated_J[k][x])

# Plot optimal and sub-optimal J_0(x) values
labels = np.array(list(range(0, len(problem.X))))
plt.bar(labels - 0.2, optimal_J, width = 0.4)
plt.bar(labels + 0.2, suboptimal_J, width = 0.4)
# Set other graph settings
plt.ylabel('Cost-to-go function J_0(x)'.format(k, k))
plt.xlabel('Feasible states at stage {}'.format(k))
plt.savefig('graphs/bar_{}_{}.png'.format(problem.name, k))
plt.close()

print('Exported bar graph to {}'.format('graphs/samples_{}_{}_{}.png'.format(problem.name, k, x)))