# Environment class with constant food resources for every round - feel free to modify as needed
class Environment(object):
    resources = 10  # food available each round
    resource_gain = 0 # food produced at the end of each round

    def __init__(self, food, gain=None):
        self.resources = food
        if gain == None:
            gain = food/2 # TODO test and adjust if needed
        self.resource_gain = gain

        

    def __repr__(self):
        # method for string representing the environment

        return ' '.join(["[", "Resources available:", str(self.resources),  "]"])
