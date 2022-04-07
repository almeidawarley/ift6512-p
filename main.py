import argparse as ag
import instance as it
import backward as bd
import parametric as pd
import time as tm
import datetime as dt

parser = ag.ArgumentParser(description = 'Compute backward and parametric policies for some instance')
parser.add_argument('folder', type = str, help = 'Path to the folder with instance files')
parser.add_argument('-s', '--samples', type = int, help = 'Set number of samples (0 means full enumeration)', default = 0)
parser.add_argument('-d', '--decay', type = int, help = 'Set rationality decay parameter (1 means fully rational)', default = 1)
parser.add_argument('--backward', action = 'store_true', help = 'Run the backward solver for the selected instance', default = False)
parser.add_argument('--parametric', action = 'store_true', help = 'Run the parametric solver for the selected instance', default = False)
parser.add_argument('--verbose', action = 'store_true', help = 'Print detailed computations when training and running the solvers', default = False)
parser.add_argument('--policies', action = 'store_true', help = 'Print policies found by the solvers in textual format', default = False)
parser.add_argument('--export', action = 'store_true', help = 'Export policies found by the solvers to a file', default = False)
arguments = parser.parse_args()

start_time = tm.time()
print('>>> Starting script at time {}'.format(dt.datetime.now()))

print('\n--------------------- Instance -----------------------\n')

# Create instance object
problem = it.Instance(arguments.folder, arguments.samples, arguments.decay)

if arguments.backward:

    print('\n--------------------- Backward -----------------------\n')

    # Run backward solver for the instance
    backward_solver = bd.Backward(problem)
    backward_solver.run_solver(arguments.verbose)
    if arguments.policies:
        backward_solver.print_policy()
    if arguments.export:
        backward_solver.export_policy()
    backward_solver.print_summary()

if arguments.parametric:

    print('\n-------------------- Parametric ----------------------\n')

    # Run parametric solver for the instance
    parametric_solver = pd.Parametric(problem)
    parametric_solver.train_solver(arguments.verbose)
    parametric_solver.run_solver(arguments.verbose)
    if arguments.policies:
        parametric_solver.print_policy()
    if arguments.export:
        parametric_solver.export_policy()
    parametric_solver.print_summary()

print('\n------------------- Information ----------------------\n')

print('If nothing has been done, type python main.py --help for help\n')

end_time = tm.time()
print('>>> Ending script at time {}'.format(dt.datetime.now()))
print('>>> Elapsed time within the script: {} seconds'.format(round(end_time - start_time, 4)))