import instance as it
import backward as bd
import parametric as pd
import matplotlib.pyplot as plt

folder = 'instances/large'
method = 'backward'
samples = 500

problem = it.Instance(folder, samples, samples)

ds = list(range(2, 5))

bJs = {}

for x in problem.X:
    bJs[x] = []

for d in ds:

    problem.d = d

    if method == 'parametric':
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
    if method == 'parametric':
        plt.plot(ds, bJs[x], '-x', label = 'J̃_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)
    else:
        plt.plot(ds, bJs[x], '-x', label = 'J_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)

plt.xlabel('Rationality decay parameter d')
if method == 'parametric':
    plt.ylabel('Approximate cost-to-go function J̃_0(x)')
else:
    plt.ylabel('Optimal cost-to-go function J_0(x)')
plt.legend(loc = 'upper right')
plt.savefig('{}_{}_decay.png'.format(method, folder.replace('instances/', '')))

plt.close()