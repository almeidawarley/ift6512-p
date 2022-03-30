import random as rd

class Backward:

    def __init__(self, instance):
        """"
            Create Backward solver for some problem instance
        """

        self.I = instance
        self.stored_J = {}
        self.stored_u = {}

    def run_solver(self):
        """"
            Solve the problem instance with Backward solver
        """

        for k in reversed(self.I.K):

            self.stored_J[k] = {}
            self.stored_u[k] = {}

            for x in self.I.X:

                if k == self.I.N:

                    y = [x] if x != self.I.empty else []

                    self.stored_J[k][x] = self.I.m(y)
                    self.stored_u[k][x] = -1

                else:

                    minimum = self.g(k, x, self.I.empty)
                    action = self.I.empty

                    # print('\tAction: {}, objective: {}'.format(action, minimum))

                    for u in self.I.U(x):

                        local = self.g(k, x, u)

                        # print('\tAction: {}, objective: {}'.format(u, local))

                        if local < minimum:
                            minimum = local
                            action = u

                    self.stored_J[k][x] = minimum
                    self.stored_u[k][x] = action
            
            if k == 3:
                _ = input('wait...')

    def g(self, k, x, u):
        """"
            Compute expectation portion of the objective function
        """

        y = [x] if x != self.I.empty else []

        cost = self.I.m(y)

        for w in self.I.W[k]:

            y_next = self.I.f(y, u, w)

            cost -= self.I.p(k, w, y) * self.I.r(y_next, w)

            x_next = self.I.empty if len(y_next) == 0 else y_next[0]

            cost += self.stored_J[k+1][x_next]

        return cost

    def print_policy(self):
        """"
            Print optimal policy found by Backward solver
        """
        
        for k in self.I.K:

            print('Stage k = {}'.format(k))

            for x in self.I.X:

                print('\tFrom location {}, go to location {}'.format(x, self.stored_u[k][x]))

