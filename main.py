import sys
import instance as it
import backward as bd

problem = it.Instance('instances/{}'.format(sys.argv[1]))

solver = bd.Backward(problem)
solver.run_solver()
solver.print_policy()