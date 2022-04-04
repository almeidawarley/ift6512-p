import instance as it
import backward as bd
import parametric as pd
import matplotlib.pyplot as plt

folder = 'instances/medium'

problem = it.Instance(folder, 0, 1)

ds = list(range(2, 21))

bJs = {}

for x in problem.X:
    bJs[x] = []

for d in ds:

    problem.d = d

    # solver = bd.Backward(problem)
    solver = pd.Parametric(problem)
    solver.train_solver()
    solver.run_solver()

    k = 0
    for x in problem.X:
        bJs[x].append(solver.J(k, x))

color = {
    '0': 'red',
    '1': 'blue',
    '2': 'yellow',
    '3': 'green',
    '4': 'orange'
}

for x in problem.X:
    plt.plot(ds, bJs[x], '-x', label = 'J̃_0({})'.format(x), color = color[x]) #, linewidth = 4, markersize = 10, zorder = 1)

plt.xlabel('Rationality decay parameter d')
plt.ylabel('Approximate cost-to-go function J̃_0(x)')
plt.legend(loc = 'upper right')

plt.show()

plt.savefig('parametric_medium_decay.png')
plt.close()