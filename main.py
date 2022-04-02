import sys
import instance as it
import backward as bd
import parametric as pd
import comparator as cp

print('###################### Starting ########################')

problem = it.Instance('instances/{}'.format(sys.argv[1]))

print('\n--------------------- Backward -----------------------')

backward_solver = bd.Backward(problem)
backward_solver.run_solver()
backward_solver.print_policy()

print('\n--------------------- Backward -----------------------')

print('\n-------------------- Parametric ----------------------')

parametric_solver = pd.Parametric(problem)
parametric_solver.train_solver()
parametric_solver.run_solver()
parametric_solver.print_policy()

print('\n-------------------- Parametric ----------------------')

print('\n-------------------- Comparator ----------------------')

comparator = cp.Comparator(problem, backward_solver, parametric_solver)
comparator.run_comparison()

print('\n-------------------- Comparator ----------------------')

print('\n******************** Technical ***********************')

parametric_solver.show_parameters()

print('\n******************** Technical ***********************')

print('\n##################### Finishing #######################')