class Comparator:

    def __init__(self, instance, backward_solver, parametric_solver):
        """"
            Create comparator object for an instance with some solvers
        """

        self.problem = instance
        self.backward = backward_solver
        self.parametric = parametric_solver
        
        pass

    def run_comparison(self):
        """"
            Run matching process for an instance with some solvers
        """

        print('Comparing backward solver with parametric solver')

        for k in self.problem.K:

            print('\tStage: {}'.format(k))

            if k != self.problem.N:

                for x in self.problem.X:
                    
                    print('\t\tState: {}'.format(x))

                    for u in self.problem.U(x):

                        print('\t\t\tAction: {}'.format(u))

                        backward_Q = self.backward.Q(k, x, u)

                        parametric_Q = self.parametric.Q(k, x, u)

                        print('\t\t\t\tBackward Q: {}'.format(backward_Q))
                        print('\t\t\t\tParametric Q: {}'.format(parametric_Q))
                        print('\t\t\t\tError: {}'.format(backward_Q - parametric_Q))

        pass