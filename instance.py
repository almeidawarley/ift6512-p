import random as rd
from re import I
import pandas as pd
import os

class Instance:

    def __init__(self, folder):
        """"
            Read instance information from file and validate it
        """

        self.read_instance(folder)
        self.check_assumptions()

    def read_instance(self, folder):
        """"
            Read instance information from file
        """

        self.name = os.path.basename(folder)

        if not os.path.isdir(folder):
            quit('Instance reading error: {} is not a valid folder'.format(folder))

        metadata_path = os.path.join(folder, 'metadata.txt')
        locations_path = os.path.join(folder, 'locations.csv')
        customers_path = os.path.join(folder, 'customers.csv')
        revenues_path = os.path.join(folder, 'revenues.csv')

        if not os.path.exists(metadata_path):
            quit('Instance reading error: {} does not exist'.format(metadata_path))

        if not os.path.exists(locations_path):
            quit('Instance reading error: {} does not exist'.format(locations_path))

        if not os.path.exists(customers_path):
            quit('Instance reading error: {} does not exist'.format(customers_path))

        if not os.path.exists(revenues_path):
            quit('Instance reading error: {} does not exist'.format(revenues_path))

        with open(metadata_path) as content:
            self.N = int(content.readline())
            self.L = content.readline().split(',')
            self.C = content.readline().split(',')
            self.S = int(content.readline())
            
        self.L = [i.strip() for i in self.L]
        self.C = [j.strip() for j in self.C]

        locations_data = pd.read_csv(locations_path)

        if len(locations_data) != len(self.L):
            quit('Instance reading error: {} is missing entries'.format(locations_path))

        self._m = {}

        for _, row in locations_data.iterrows():
            self._m[str(row['id'])] = int(row['m'])

        customers_data = pd.read_csv(customers_path)

        if len(customers_data) != len(self.C):
            quit('Instance reading error: {} is missing entries'.format(customers_path))

        if len(customers_data.columns) - 1!= len(self.L):
            quit('Instance reading error: {} is missing columns'.format(customers_path))

        self.rank = {}

        for _, row in customers_data.iterrows():
            self.rank[str(row['id'])] = []
            for index, _ in enumerate(self.L):
                self.rank[str(row['id'])].append(str(row[str(index + 1)]))
        
        revenues_data = pd.read_csv(revenues_path)

        if len(revenues_data) != len(self.C):
            quit('Instance reading error: {} is missing entries'.format(revenues_path))

        if len(revenues_data.columns) - 1!= len(self.L):
            quit('Instance reading error: {} is missing columns'.format(revenues_path))

        self._r = {}

        for _, row in revenues_data.iterrows():
            self._r[str(row['id'])] = {}
            for index, _ in enumerate(self.L):
                self._r[str(row['id'])][str(index + 1)] = float(row[str(index + 1)])

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
            quit('Value computation error: {} is not a subset of {}'.format(y_k, self.L))

        if not set(w_k).issubset(self.L):
            quit('Value computation error: {} is not a subset of {}'.format(w_k, self.L))

        revenue = .0

        for j in self.C:
            for i in self.rank[j]:
                if i in y_k or i in w_k:
                    revenue += self._r[j][i] if i in y_k else .0
                    break

        return revenue

    def m(self, y_k):
        """
            Compute maintenance for company with y_k
        """

        maintenance = .0

        for i in y_k:
            maintenance += self._m[i]

        return maintenance