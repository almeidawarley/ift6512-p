import argparse as ag
import instance as it
import backward as bd
import parametric as pd
import matplotlib.pyplot as plt

parser = ag.ArgumentParser(description = 'Create graphs with varying rationality decay parameter for an instance of the multi-period competitive facility location problem of temporary retail faciltiies')
parser.add_argument('folder', type = str, help = 'Path to the folder containing files with the instance information')
parser.add_argument('solver', type = str, help = 'Name of the solver used to generate the optimal policy')
parser.add_argument('max_decay', type = int, help = 'Maximum value for the rationality decay parameter')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples of the random variable (0 means complete enumeration)', default = 0)
arguments = parser.parse_args()

problem = it.Instance(arguments.folder, arguments.samples, 1)

ds = [1, 1.2, 1.4, 1.6, 1.8] + list(range(2, arguments.max_decay + 1))

bJs = {}

for x in problem.X:
    bJs[x] = []

for d in ds:

    problem.d = d

    if arguments.solver == 'parametric':
        solver = pd.Parametric(problem)
        solver.train_solver()
    else:
        solver = bd.Backward(problem)

    solver.run_solver(True)

    k = 0
    for x in problem.X:
        bJs[x].append(solver.J(k, x))

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

for x in problem.X:
    if arguments.solver == 'parametric':
        plt.plot(ds, bJs[x], '-x', label = 'J̃_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)
    else:
        plt.plot(ds, bJs[x], '-x', label = 'J_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)

plt.xlabel('Rationality decay parameter d')
if arguments.solver == 'parametric':
    plt.ylabel('Approximate cost-to-go function J̃_0(x)')
else:
    plt.ylabel('Optimal cost-to-go function J_0(x)')
plt.legend(loc = 'upper right')
plt.savefig('graphs/{}_{}_decay.png'.format(arguments.solver, problem.name))

plt.close()