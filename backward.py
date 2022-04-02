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

            print('\tStage {}'.format(k))

            for x in self.I.X:

                if k == self.I.N:

                    y = [x] if x != self.I.empty else []

                    self.stored_J[k][x] = self.I.m(k, y)
                    self.stored_u[k][x] = -1

                else:

                    print('\t\tState {}'.format(x))

                    U = self.I.U(x)

                    minimum = self.Q(k, x, U[0])
                    action = U[0]

                    for u in U:

                        local = self.Q(k, x, u)

                        print('\t\t\tAction {} -> Q value {}'.format(u, round(local, 2)))

                        if local < minimum:
                            minimum = local
                            action = u

                    self.stored_J[k][x] = minimum
                    self.stored_u[k][x] = action

    def Q(self, k, x, u):
        """"
            Compute expectation portion of the objective function
        """

        y = [x] if x != self.I.empty else []

        cost = self.I.m(k, y)

        for w in self.I.W[k]:

            p = self.I.p(k, w, y)

            # TASK: add condition p > .00001

            y_next = self.I.f(y, u, w)

            x_next = self.I.empty if len(y_next) == 0 else y_next[0]

            cost -= p * self.I.r(y_next, w) # + self.I.t(x, x_next)

            cost += p * self.stored_J[k+1][x_next]

        return cost

    def print_policy(self):
        """"
            Print optimal policy found by Backward solver
        """
        
        for k in self.I.K:

            print('Stage k = {}'.format(k))

            for x in self.I.X:

                print('\tFrom location {}, go to location {}'.format(x, self.stored_u[k][x]))