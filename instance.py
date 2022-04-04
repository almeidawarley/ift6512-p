import scipy.special as sp
import itertools as tl
import random as rd
import pandas as pd
import os

class Instance:

    def __init__(self, folder):
        """"
            Read instance information from file and validate it
        """

        rd.seed(100)

        self.read_instance(folder)
        self.check_assumptions()

    def read_instance(self, folder, apply_sampling = False):
        """"
            Read instance information from file
        """

        self.name = os.path.basename(folder)

        if not os.path.isdir(folder):
            raise Exception('Instance reading error: {} is not a valid folder'.format(folder))

        metadata_path = os.path.join(folder, 'metadata.txt')
        locations_path = os.path.join(folder, 'locations.csv')
        customers_path = os.path.join(folder, 'customers.csv')
        revenues_path = os.path.join(folder, 'revenues.csv')

        if not os.path.exists(metadata_path):
            raise Exception('Instance reading error: {} does not exist'.format(metadata_path))

        if not os.path.exists(locations_path):
            raise Exception('Instance reading error: {} does not exist'.format(locations_path))

        if not os.path.exists(customers_path):
            raise Exception('Instance reading error: {} does not exist'.format(customers_path))

        if not os.path.exists(revenues_path):
            raise Exception('Instance reading error: {} does not exist'.format(revenues_path))

        with open(metadata_path) as content:
            self.N = int(content.readline())
            self.L = content.readline().split(',')
            self.C = content.readline().split(',')
            self.S = int(content.readline())
            self.d = int(content.readline())
            
        self.L = [i.strip() for i in self.L]
        self.C = [j.strip() for j in self.C]
        self.K = list(range(0, self.N + 1))

        locations_data = pd.read_csv(locations_path)

        if len(locations_data) != len(self.L):
            raise Exception('Instance reading error: {} is missing entries'.format(locations_path))

        self._m = {}

        for _, row in locations_data.iterrows():
            self._m[str(row['id'])] = int(row['m'])

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

        if apply_sampling:
            self.W = { k : self.sample_scenarios() for k in self.K if k != self.N }
        else:
            self.W = { k : self.list_scenarios() for k in self.K if k != self.N }

        self.empty = '0'

        self.X = [self.empty] + self.L

    def list_scenarios(self):
        """
            List all scenarios for competitor activations
        """

        samples = []

        for size in range(0, len(self.L) + 1):
            
            local = tl.combinations(self.L, size)
            samples += [list(e) for e in local]

        return samples

    def sample_scenarios(self):
        """
            Sample s scenarios for competitor activations
        """

        samples = []

        counter = 0
        
        while counter <= self.S:
            
            sizes = range(0, len(self.L) + 1)

            size = rd.sample(sizes, 1)[0]

            sample = sorted(rd.sample(self.L, size))

            if sample not in samples:
                samples.append(sample)
                counter += 1

        return samples

    def check_assumptions(self):
        """
            Check assumptions about the instance information
        """

        pass

    def __str__(self):
        """"
            Translate instance object into a string
        """

        payload = '\n*-------------------------------------------------------------------------*\n\n'
        payload += '\tInstance name: {}\n'.format(self.name)
        payload += '\tSet of locations: {}\n'.format(self.L)
        payload += '\tSet of customers: {}\n'.format(self.C)
        payload += '\tCustomer preferences:\n'
        for j in self.C:
            payload += '\t\tCustomer {}: '.format(j)
            for index, _ in enumerate(self.L):
                payload += '{} ({}) {} '.format(self.rank[j][index], self._r[j][self.rank[j][index]], '>' if index != len(self.L) - 1 else '\n')
        payload += '\tNumber of periods: {}\n'.format(self.N)
        payload += '\tNumber of samples: {}\n'.format(self.S)
        payload += '\n*-------------------------------------------------------------------------*\n\n'

        return payload

    def r(self, y_k, w_k):
        """
            Compute revenue for company with activation y_k when competitors have activation w_k
        """

        if not set(y_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(y_k, self.L))

        if not set(w_k).issubset(self.L):
            raise Exception('Value computation error: {} is not a subset of {}'.format(w_k, self.L))

        revenue = .0

        for j in self.C:
            for i in self.rank[j]:
                if i in y_k or i in w_k:
                    revenue += self._r[j][i] if i in y_k else .0
                    break

        return revenue

    def m(self, k, y_k):
        """
            Compute maintenance for company with activation y_k
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

    def t(self, x_k, x_next):
        """
            Compute transportation from activation at x_k to activation at x_next
        """

        return self._t[x_k][x_next]

    def f(self, y_k, u_k, w_k):
        """
            Compute transition function for activation y_k, action u_k, and realization w_k
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
            Compute probability of activation w_k given activation y_k at stage k
        """

        return self.profitability(k, w_k, y_k)

    def profitability(self, k, w_k, y_k):
        """
            Compute probability of activation w_k based on profitability
        """

        x_k = y_k[0] if len(y_k) == 1 else None

        if x_k in w_k:
            return .0

        omega = [w for w in self.W[k] if x_k not in w]

        index = omega.index(w_k)

        beta = 1 / self.d ** k

        profits = [beta * (self.r(w, y_k) - self.m(k, w)) for w in omega]

        exp = sp.softmax(profits)

        return exp[index]

    def U(self, x_k):

        return [i for i in self.L if i != x_k]

    def phi(self, k, x_k, u_k):

        features = []

        '''

        # Option 1

        features += [k]

        features += [1 if x_k == self.empty else 0]

        for index, _ in enumerate(self.L):
            
            C = [1 for j in self.C if self.rank[j][index] == x_k]

            features += [sum(C)]

            # features += [mt.exp(sum(C))]

            C = [1 for j in self.C if self.rank[j][index] == u_k]

            features += [sum(C)]

            # features += [mt.exp(sum(C))]

        features += [self.rank[j].index(x_k) - self.rank[j].index(u_k) if x_k != self.empty else len(self.L) + 1 for j in self.C]

        '''

        '''
        
        # Option 2

        features += [1 if x_k == self.empty else 0]

        features += [self._m[x_k] if x_k != self.empty else 0]
        features += [self._m[u_k]]

        features += [self._r[j][x_k] if x_k != self.empty else 0 for j in self.C]

        features += [self._r[j][u_k] for j in self.C]

        '''

        for w in self.L:

            y_k = [x_k] if x_k != self.empty else []

            features += [self.r(y_k, [w])]
            
            features += [self.m(k, y_k)]

            z_k = [u_k]

            features += [self.r(z_k, [w])]
            
            features += [self.m(k, z_k)]

        return features

    def dummy(self):

        return [1 for _ in self.phi(0, self.empty, '1')]
