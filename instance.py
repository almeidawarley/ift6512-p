import scipy.special as sp
import itertools as tl
import random as rd
import pandas as pd
import os

class Instance:

    def __init__(self, folder, samples, decay):
        """
            Create instance object based on arguments
        """

        # rd.seed(100)

        self.read_instance(folder, samples, decay)

    def read_instance(self, folder, samples, decay):
        """
            Read instance information from file
        """

        print('Reading instance from folder {}'.format(folder))

        # Retrieve the name of the instance (small, medium, or large)
        self.name = os.path.basename(folder)

        if not os.path.isdir(folder):
            raise Exception('Instance reading error: {} is not a valid folder'.format(folder))

        # Create path of instance information files
        metadata_path = os.path.join(folder, 'metadata.txt')
        locations_path = os.path.join(folder, 'locations.csv')
        customers_path = os.path.join(folder, 'customers.csv')
        revenues_path = os.path.join(folder, 'revenues.csv')

        # Check if these files exist or not
        if not os.path.exists(metadata_path):
            raise Exception('Instance reading error: {} does not exist'.format(metadata_path))
        if not os.path.exists(locations_path):
            raise Exception('Instance reading error: {} does not exist'.format(locations_path))
        if not os.path.exists(customers_path):
            raise Exception('Instance reading error: {} does not exist'.format(customers_path))
        if not os.path.exists(revenues_path):
            raise Exception('Instance reading error: {} does not exist'.format(revenues_path))

        # Read sets of locations and customers from metadata
        # Read number of time periods from metadata too
        with open(metadata_path) as content:
            self.N = int(content.readline())
            self.L = content.readline().split(',')
            self.C = content.readline().split(',')

        # Format sets of locations and customers
        self.L = [i.strip() for i in self.L]
        self.C = [j.strip() for j in self.C]
        # Create set of time periods K
        self.K = list(range(0, self.N + 1))

        # Read maintenance costs for locations
        locations_data = pd.read_csv(locations_path)
        if len(locations_data) != len(self.L):
            raise Exception('Instance reading error: {} is missing entries'.format(locations_path))
        self._m = {}
        for _, row in locations_data.iterrows():
            self._m[str(row['id'])] = int(row['m'])

        # Read rankings of customers
        customers_data = pd.read_csv(customers_path)
        if len(customers_data) != len(self.C):
            raise Exception('Instance reading error: {} is missing entries'.format(customers_path))
        if len(customers_data.columns) - 1!= len(self.L):
            raise Exception('Instance reading error: {} is missing columns'.format(customers_path))
        self.rank = {}
        for _, row in customers_data.iterrows():
            self.rank[str(row['id'])] = []
            for index, _ in enumerate(self.L):
                self.rank[str(row['id'])].append(str(row[str(index + 1)]))

        # Read estimated revenues of customers per location
        revenues_data = pd.read_csv(revenues_path)
        if len(revenues_data) != len(self.C):
            raise Exception('Instance reading error: {} is missing entries'.format(revenues_path))
        if len(revenues_data.columns) - 1!= len(self.L):
            raise Exception('Instance reading error: {} is missing columns'.format(revenues_path))
        self._r = {}
        for _, row in revenues_data.iterrows():
            self._r[str(row['id'])] = {}
            for index, _ in enumerate(self.L):
                self._r[str(row['id'])][str(index + 1)] = float(row[str(index + 1)])

        # Sample scenarios per time period according to parameter s
        self.s = samples
        if self.s > 0:
            if self.s >= 2**len(self.L):
                valid = int(round(0.9 * 2**len(self.L)))
                print('Adjusting number of samples from {} to {}'.format(self.s, valid))
                self.s = valid
            self.W = { k : self.sample_scenarios() for k in self.K if k != self.N }
        else:
            self.W = { k : self.list_scenarios() for k in self.K if k != self.N }

        # Set name of empty state (i.e., 0)
        self.empty = '0'

        # Set rationality decay parameter
        self.d = decay

        # Create set of feasible states
        self.X = [self.empty] + self.L

        # print(self)

    def list_scenarios(self):
        """
            List all scenarios for competitor locations
        """

        samples = []

        for size in range(0, len(self.L) + 1):

            # List combinations of locations with a certain size
            local = tl.combinations(self.L, size)
            # Append this list of combinations to the samples
            samples += [list(e) for e in local]

        return samples

    def sample_scenarios(self):
        """
            Sample s scenarios for competitor locations
        """

        samples = []

        counter = 0

        while counter <= self.s:

            # Choose a random size for the combination
            sizes = range(0, len(self.L) + 1)
            size = rd.sample(sizes, 1)[0]

            # Sort elements to avoid repetition
            sample = sorted(rd.sample(self.L, size))

            # Check if sample has already been sampled
            if sample not in samples:
                samples.append(sample)
                counter += 1

        return samples

    def __str__(self):
        """
            Translate instance object into a string
        """

        payload = '\n*----------------------------------------------------*\n\n'
        payload += '\tInstance name: {}\n'.format(self.name)
        payload += '\tSet of locations: {}\n'.format(self.L)
        payload += '\tSet of customers: {}\n'.format(self.C)
        payload += '\tLocation maintenance:\n'
        for i in self.L:
            payload += '\t\tLocation {}: {}\n'.format(i, self._m[i])
        payload += '\tCustomer preferences:\n'
        for j in self.C:
            payload += '\t\tCustomer {}: '.format(j)
            for index, _ in enumerate(self.L):
                payload += '{} ({}) {} '.format(self.rank[j][index], self._r[j][self.rank[j][index]], '>' if index != len(self.L) - 1 else '\n')
        payload += '\tNumber of periods: {}\n'.format(self.N)
        payload += '\tNumber of samples: {}\n'.format(self.s)
        payload += '\tRationality decay: {}\n'.format(self.d)
        payload += '\n*---------------------------------------------------*\n\n'

        return payload

    def r(self, y_k, w_k):
        """
            Compute the revenue of the company with locations y_k competing against competitors with locations w_k
        """

        if not set(y_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(y_k, self.L))

        if not set(w_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(w_k, self.L))

        revenue = .0

        # Compute the revenue of the company accordingly
        for j in self.C:
            for i in self.rank[j]:
                if i in y_k or i in w_k:
                    revenue += self._r[j][i] if i in y_k else .0
                    break

        return revenue

    def m(self, k, y_k):
        """
            Compute the maintenance cost for the company with locations y_k at stage k
        """

        if k == 0:
            return .0

        if not set(y_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(y_k, self.L))

        if len(y_k) == 0:
            return 0

        maintenance = .0

        for i in y_k:
            maintenance += self._m[i]

        return maintenance

    def f(self, y_k, u_k, w_k):
        """
            Compute transition function for location y_k, action u_k, and realization w_k
        """

        if not set([u_k]).issubset(self.L + [self.empty]):
            raise Exception('Value computation error: {} is not a subset of {}'.format(u_k, self.L))

        if not set(w_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(w_k, self.L))

        if u_k == self.empty:
            return []
        elif u_k in w_k:
            return []
        else:
            return [u_k]

    def p(self, k, w_k, y_k):
        """
            Compute the probability of having competitor locations w_k with location y_k
        """

        return self.profitability(k, w_k, y_k)

    def profitability(self, k, w_k, y_k):
        """
            Compute pthe robability of having competitor locations w_k with location y_k based on profitability
        """

        x_k = y_k[0] if len(y_k) == 1 else None

        # Filter realizations w_k that have location x_k as an element
        # (i.e., competitors do not perceive location x_k as avaialble)
        if x_k in w_k:
            return .0

        omega = [w for w in self.W[k] if x_k not in w]

        index = omega.index(w_k)

        # Compute beta based on rationality decay parameter
        beta = 1 / self.d ** k

        # Compute potential profits to pass to the softmax
        profits = [beta * (self.r(w, y_k) - self.m(k, w)) for w in omega]

        exp = sp.softmax(profits)

        return exp[index]

    def U(self, x_k):
        """
            Compute the set of feasible actions when the company is at location x_k
        """

        return [i for i in self.L if i != x_k]

    def phi(self, k, x_k, u_k):
        """
            Compute the feature vector based on location x_k and location u_k
        """

        features = []

        # Create first set of features: distance between locations x_k and u_k for customer profile j
        features += [self.rank[j].index(x_k) - self.rank[j].index(u_k) if x_k != self.empty else len(self.L) + 1 for j in self.C]

        y_k = [x_k] if x_k != self.empty else []
        z_k = [u_k]

        # Create second set of features: revenues for locations x_k and u_k competing one competitor location w
        for w in self.L:

            features += [self.r(y_k, [w])]

            features += [self.r(z_k, [w])]

        # Create third set of features: maintenance for locations x_k and u_k
        features += [self.m(k, y_k)]
        features += [self.m(k, z_k)]

        return features

    def dummy(self):
        """
            Create a dummy starting coefficient for the parametric solver
        """

        return [1 for _ in self.phi(0, self.empty, '1')]
