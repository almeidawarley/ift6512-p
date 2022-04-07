import numpy as np
import scipy.optimize as sp
import uuid

class Parametric:

    def __init__(self, instance):
        """
            Create Parametric solver for some problem instance
        """

        # Store instance object
        self.I = instance
        # Store r_k coefficients
        self.stored_r = {}
        # Store \mu_k(x) values
        self.stored_u = {}

    def train_solver(self, verbose = False):
        """
            Train a linear architecture for the Parametric solver
        """

        print('Training parametric solver')

        # Loop over planning stages
        for k in reversed(self.I.K):

            if k != self.I.N:

                # Create function to be minimized using least squares
                def to_minimize(r, points, labels):

                    return [np.dot(r, point) - label for point, label in zip(points, labels)]

                # Retrieve dummy coefficients r0 as starting point
                r0 = self.I.dummy()

                # Create list of points based on states x and actions u
                points = [self.I.phi(k, x, u) for x in self.I.X for u in self.I.U(x)]

                # Double the list of points to make sure there is enough
                points += points

                # Create list of labels based on the \hat{Q}_k(x,u) function
                labels = [self.Qhat(k, x, u) for x in self.I.X for u in self.I.U(x)]

                # Double the list of labels to make sure there is enough
                labels += labels

                # Call the least squares minimizer
                report = sp.leastsq(to_minimize, r0, (points, labels))

                # Export the data used for the training
                with open('training/{}_{}.csv'.format(self.I.name, k), 'w') as output:
                    for i, _ in enumerate(points):
                        # Formtat as (label, point) in a CSV file
                        output.write('{},{}\n'.format(labels[i], ','.join([str(e) for e in points[i]])))

                # Store the r_k coefficient trained in this stage
                self.stored_r[k] = report[0]

        if verbose:
            print('Parameters of linear architecture:')
            for k in self.I.K:
                if k != self.I.N:
                    print('\tStage {}: {}'.format(k, self.stored_r[k]))


    def run_solver(self, verbose = False):
        """
            Solve the problem instance with Parametric solver
        """

        print('Running parametric solver')

        # Loop over planning stages
        for k in self.I.K:

            if verbose:
                print('\tStage {}'.format(k))

            self.stored_u[k] = {}

            # Loop over feasible states
            for x in self.I.X:

                if k == self.I.N:

                    # No action to take at stage k
                    self.stored_u[k][x] = -1

                else:

                    if verbose:
                        print('\t\tState {}'.format(x))

                    # Compute optimal \tilde{Q}_k(x,u) k < N

                    U = self.I.U(x)

                    minimum = self.Qtilde(k, x, U[0])
                    action = U[0]

                    # Loop over feasible actions
                    for u in U:

                        local = self.Qtilde(k, x, u)

                        if verbose:
                            print('\t\t\tAction {} -> Qtilde_{}({}, {}) = {}'.format(u, k, x, u, round(local, 2)))

                        if local < minimum:
                            minimum = local
                            action = u

                    self.stored_u[k][x] = action

    def Qhat(self, k, x, u):
        """
            Compute the \hat{Q}_k(x,u) value with the expectation term
        """

        y = [x] if x != self.I.empty else []

        if k == self.I.N:
            quit('Function Q has been wrongly called for time period {}'.format(k))


        # Compute the deterministic term
        cost = self.I.m(k, y)

        # Compute the expectation term
        for w in self.I.W[k]:

            p = self.I.p(k, w, y)

            if p > 0.0001:

                y_next = self.I.f(y, u, w)

                x_next = self.I.empty if len(y_next) == 0 else y_next[0]

                cost -= p * self.I.r(y_next, w) # + self.I.t(x, x_next)

                # Retrieve J_{k+1}(x) through \tilde{Q}_{k+1}(x,u)

                U  = self.I.U(x_next)

                minimum = self.Qtilde(k + 1, x_next, U[0])

                for u_next in self.I.U(x_next):

                    local = self.Qtilde(k + 1, x_next, u_next)

                    if local < minimum:

                        minimum = local

                cost += p * minimum

        return cost

    def Qtilde(self, k, x, u):
        """
            Compute the \tilde{Q}_k(x,u) value with the linear approximation
        """

        y = [x] if x != self.I.empty else []

        if k == self.I.N:
            return self.I.m(k, y)

        phi = self.I.phi(k, x, u)

        return np.dot(self.stored_r[k], phi)

    def Jtilde(self, k, x):
        """
            Compute the \tilde{J}_k(x) value for the stored policy
        """

        return self.Qtilde(k, x, self.stored_u[k][x])

    def print_policy(self):
        """
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
        """
            Export sub-optimal policy found by Parametric solver
        """

        print('Exporting parametric policy')

        with open('policies/parametric_{}_{}_{}_{}.txt'.format(self.I.name, self.I.s, self.I.d, str(uuid.uuid4())[:8]),'w') as output:

            output.write('{}'.format(self.stored_u))

    def print_summary(self, k = 0):
        """
            Print summary of the Parametric solver for stage k
        """

        for x in self.I.X:
            print('\tThe expected profit Jtilde_{}({}) is {}'.format(k, x, self.Jtilde(k, x)))