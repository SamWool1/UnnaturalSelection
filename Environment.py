# Environment class with constant food resources for every round - feel free to modify as needed
class Environment(object):
    resources = 10  # food available each round

    def __init__(self, food):
        self.resources = food

    def __repr__(self):
        # method for string representing the environment

        return ' '.join(["[", "Resources available:", str(self.resources),  "]"])