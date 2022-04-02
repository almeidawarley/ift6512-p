import sys
import instance as it
import backward as bd
import parametric as pd

problem = it.Instance('instances/{}'.format(sys.argv[1]))

print('--------------------- Backward -----------------------')

backward_solver = bd.Backward(problem)
backward_solver.run_solver()
backward_solver.print_policy()

_ = input('Press enter to move forward')

print('-------------------- Parametric ----------------------')

parametric_solver = pd.Parametric(problem)
parametric_solver.train_solver()
parametric_solver.run_solver()
parametric_solver.print_policy()

_ = input('Press enter to move forward')

print('******************** Technical ***********************')

parametric_solver.show_parameters()

_ = input('Press enter to move forward')