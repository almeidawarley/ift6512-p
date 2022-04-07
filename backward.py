import uuid

class Backward:

    def __init__(self, instance):
        """
            Create Backward solver for some problem instance
        """

        # Store instance object
        self.I = instance
        # Store J_k(x) values
        self.stored_J = {}
        # Store \mu_k(x) values
        self.stored_u = {}

    def run_solver(self, verbose = False):
        """
            Solve the problem instance with Backward solver
        """

        print('Running backward solver')

        # Loop over planning stages
        for k in reversed(self.I.K):

            self.stored_J[k] = {}
            self.stored_u[k] = {}

            if verbose:
                print('\tStage {}'.format(k))

            # Loop over feasible states
            for x in self.I.X:

                if k == self.I.N:

                    # Compute g_N(x) if at stage k = N

                    y = [x] if x != self.I.empty else []

                    self.stored_J[k][x] = self.I.m(k, y)
                    self.stored_u[k][x] = -1

                else:

                    if verbose:
                        print('\t\tState {}'.format(x))

                    # Compute optimal Q_k(x,u) k < N

                    U = self.I.U(x)

                    minimum = self.Q(k, x, U[0])
                    action = U[0]

                    # Loop over feasible actions
                    for u in U:

                        local = self.Q(k, x, u)

                        if verbose:
                            print('\t\t\tAction {} -> Q_{}({}, {}) = {}'.format(u, k, x, u, round(local, 2)))

                        if local < minimum:
                            minimum = local
                            action = u

                    self.stored_J[k][x] = minimum
                    self.stored_u[k][x] = action

    def Q(self, k, x, u):
        """
            Compute the Q_k(x,u) value with the expectation term
        """

        y = [x] if x != self.I.empty else []

        if k == self.I.N:
            return self.I.m(k, y)

        # Compute the deterministic term
        cost = self.I.m(k, y)

        # Compute the exoectation term
        for w in self.I.W[k]:

            p = self.I.p(k, w, y)

            if p > 0.0001:

                y_next = self.I.f(y, u, w)

                x_next = self.I.empty if len(y_next) == 0 else y_next[0]

                # Compute the estimated revenue for the realization w
                cost -= p * self.I.r(y_next, w) # + self.I.t(x, x_next)

                # Weight optimal cost-to-go values until the end
                cost += p * self.stored_J[k + 1][x_next]

        return cost

    def J(self, k, x):
        """
            Compute the J_k(x) value for the stored policy
        """

        return self.Q(k, x, self.stored_u[k][x])

    def print_policy(self):
        """
            Print optimal policy found by Backward solver
        """

        print('Printing backward policy')

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
            Export optimal policy found by Backward solver
        """

        print('Exporting backward policy')

        with open('policies/backward_{}_{}_{}_{}.txt'.format(self.I.name, self.I.s, self.I.d, str(uuid.uuid4())[:8]),'w') as output:

            output.write('{}'.format(self.stored_u))

    def print_summary(self, k = 0):
        """
            Print summary of the Backward solver for stage k
        """

        for x in self.I.X:
            print('\tThe expected profit J_{}({}) is {}'.format(k, x, self.J(k, x)))

    def evaluate_policy(self, policy):
        """
            Evaluate some policy according to the information stored locally
            (useful to compare a sub-optimal policy with the optimal policy)
        """

        # print('Evaluating policy {}'.format(policy))

        evaluated_J = {}

        for k in reversed(self.I.K):

            evaluated_J[k] = {}

            # print('\tStage {}'.format(k))

            for x in self.I.X:

                if k == self.I.N:

                    y = [x] if x != self.I.empty else []

                    evaluated_J[k][x] = self.I.m(k, y)

                else:

                    # print('\t\tState {}'.format(x))

                    # Apply policy provided as argument instead of minimizing over feasible actions
                    evaluated_J[k][x] = self.Q(k, x, policy[k][x])

        return evaluated_J