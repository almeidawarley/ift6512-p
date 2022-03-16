import random as rd

class Matcher:

    def __init__(self, instance, Backward, Parametric, Rollout):
        """"
            Create matcher object for an instance with some solvers
        """

        self.problem_instance = instance
        self.backward_class = Backward
        self.parametric_class = Parametric
        self.rollout_class = Rollout
        
        pass

    def run(self):
        """"
            Run matching process for an instance with some solvers
        """

        pass