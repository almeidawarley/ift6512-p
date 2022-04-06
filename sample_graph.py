import ast
import os
import argparse as ag
import instance as it
import backward as bd
import matplotlib.pyplot as plt

parser = ag.ArgumentParser(description = 'Evaluate approximated policy for an instance of the multi-period competitive facility location problem of temporary retail faciltiies')
parser.add_argument('folder', type = str, help = 'Path to the folder containing files with the instance information')
parser.add_argument('solver', type = str, help = 'Name of the solver used to generate approximated optimal policy')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples of the random variable (0 means complete enumeration)', default = 0)
parser.add_argument('-d', '--decay', type = int, help = 'Set value of rationality decay of the competitors (1 means always fully rational)', default = 1)
arguments = parser.parse_args()

if arguments.decay <= 1:
    quit('The decay parameter d = {} should be greater than 1'.format(arguments.decay))

problem = it.Instance(arguments.folder, 0, arguments.decay)

reference = bd.Backward(problem)
reference.run_solver()

policies = []

pattern = '{}_{}_{}_{}'.format(arguments.solver, problem.name, arguments.samples, arguments.decay)

print('Looking for stored policies with pattern {}'.format(pattern))

for file in os.listdir('policies'):
    if pattern in file:
        print('\tFound policy {}'.format(file))
        with open('policies/{}'.format(file)) as output:
            content = output.read()
        policy = ast.literal_eval(content)
        policies.append(policy)

error_J = {}

for k in problem.K:
    error_J[k] = {}
    for x in problem.X:
        error_J[k][x] = []

for identifier, policy in enumerate(policies):

    print('Evaluating policy #{}'.format(identifier))

    evaluated_J = reference.evaluate_policy(policy)

    for k in problem.K:
        for x in problem.X:
            error = evaluated_J[k][x] - reference.J(k, x)
            print('\tError of J_{}({}) = {}'.format(k, x, error))
            error_J[k][x].append(error)

k = 0

data = []
label = []
for x in problem.X:
    if len(error_J[k][x]) > 0:
        data.append(error_J[k][x])
        # label.append('J_{}({})'.format(k, x))
        label.append('x = {}'.format(x))

plt.boxplot(data)
plt.xticks(range(1, len(problem.X) + 1), label)
plt.ylabel('Approximation error of cost-to-go function)'.format(k, k))
plt.xlabel('Feasible states x at stage {}'.format(k))
plt.savefig('graphs/{}_{}__{}_samples.png'.format(arguments.solver, problem.name, k))
plt.close()
