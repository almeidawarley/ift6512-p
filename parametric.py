import numpy as np
import scipy.optimize as sp
import uuid

class Parametric:

    def __init__(self, instance):
        """"
            Create Parametric solver for some problem instance
        """

        self.I = instance

        self.stored_r = {}
        self.stored_u = {}

    def train_solver(self):
        """"
            Train a linear architecture for the Parametric solver
        """

        print('Training parametric solver')

        for k in reversed(self.I.K):

            if k != self.I.N:

                def to_minimize(r, points, labels):

                    return [np.dot(r, point) - label for point, label in zip(points, labels)]

                r0 = self.I.dummy()

                points = [self.I.phi(k, x, u) for x in self.I.X for u in self.I.U(x)]

                points += points

                labels = [self.Q(k, x, u) for x in self.I.X for u in self.I.U(x)]

                labels += labels

                report = sp.leastsq(to_minimize, r0, (points, labels))

                with open('training/{}_{}.csv'.format(self.I.name, k), 'w') as output:

                    for i, _ in enumerate(points):

                        output.write('{},{}\n'.format(labels[i], ','.join([str(e) for e in points[i]])))

                self.stored_r[k] = report[0]

        print('Parameters of linear architecture:')

        for k in self.I.K:
            if k != self.I.N:
                print('\tStage {}: {}'.format(k, self.stored_r[k]))


    def run_solver(self, verbose = False):
        """"
            Solve the problem instance with Parametric solver
        """

        print('Running parametric solver')

        for k in self.I.K:

            if verbose:
                print('\tStage {}'.format(k))

            self.stored_u[k] = {}

            for x in self.I.X:

                if k == self.I.N:

                    self.stored_u[k][x] = -1

                else:

                    if verbose:
                        print('\t\tState {}'.format(x))

                    U = self.I.U(x)

                    minimum = self.Qaprox(k, x, U[0])
                    action = U[0]

                    for u in U:

                        local = self.Qaprox(k, x, u)

                        if verbose:
                            print('\t\t\tAction {} -> Q value {}'.format(u, round(local, 2)))

                        if local < minimum:
                            minimum = local
                            action = u

                    self.stored_u[k][x] = action

    def Q(self, k, x, u):
        """"
            Compute expectation portion using approximation
        """

        y = [x] if x != self.I.empty else []

        if k == self.I.N:
            quit('Function Q has been wrongly called for time period {}, abort'.format(k))

        cost = self.I.m(k, y)

        for w in self.I.W[k]:

            p = self.I.p(k, w, y)

            if p > 0.0001:

                y_next = self.I.f(y, u, w)

                x_next = self.I.empty if len(y_next) == 0 else y_next[0]

                cost -= p * self.I.r(y_next, w) # + self.I.t(x, x_next)

                U  = self.I.U(x_next)

                minimum = self.Qaprox(k + 1, x_next, U[0])

                for u_next in self.I.U(x_next):

                    local = self.Qaprox(k + 1, x_next, u_next)

                    if local < minimum:

                        minimum = local

                cost += p * minimum

        return cost

    def Qaprox(self, k, x, u):
        """"
            Compute expectation portion of the objective function
        """

        y = [x] if x != self.I.empty else []

        if k == self.I.N:
            return self.I.m(k, y)

        phi = self.I.phi(k, x, u)

        return np.dot(self.stored_r[k], phi)

    def J(self, k, x):

        return self.Qaprox(k, x, self.stored_u[k][x])

    def print_policy(self):
        """"
            Print optimal policy found by Parametric solver
        """

        print('Printing parametric policy')

        for k in self.I.K:

            print('\tStage {}'.format(k))

            if k != self.I.N:

                for x in self.I.X:

                    print('\t\tAt state {}, take action {}'.format(x, self.stored_u[k][x]))

                    transition = {}

                    for x_next in self.I.X:

                        transition[x_next] = .0

                    for w in self.I.W[k]:

                        y = [x] if x != self.I.empty else []

                        y_next = self.I.f(y, self.stored_u[k][x], w)

                        x_next = self.I.empty if len(y_next) == 0 else y_next[0]

                        p = self.I.p(k, w, y)

                        transition[x_next] += p

                    for x_next, p in transition.items():

                        if p > .0001:

                            print('\t\t\tGo to state {} with probability {}'.format(x_next, round(p, 4)))

            else:

                print('\t\tNo actions to take at the last stage')

    def export_policy(self):

        print('Exporting parametric policy')

        with open('policies/parametric_{}_{}_{}_{}.txt'.format(self.I.name, self.I.s, self.I.d, str(uuid.uuid4())[:8]),'w') as output:

            output.write('{}'.format(self.stored_u))