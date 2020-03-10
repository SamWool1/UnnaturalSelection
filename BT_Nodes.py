from copy import deepcopy

############################### Base Classes ##################################
class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state, ai):
        raise NotImplementedError

    def copy(self):
        return deepcopy(self)


class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state, ai):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''

    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        for child in self.child_nodes:
            if hasattr(child, 'tree_to_string'):
                string += child.tree_to_string(indent + 1)
            else:
                string += '| ' * (indent + 1) + str(child) + '\n'
        return string


############################### Composite Nodes ##################################
class Selector(Composite):
    def execute(self, state, ai):
        for child_node in self.child_nodes:
            success = child_node.execute(state, ai)
            if success:
                return True
        else:  # for loop completed without success; return failure
            return False


class Sequence(Composite):
    def execute(self, state, ai):
        for child_node in self.child_nodes:
            continue_execution = child_node.execute(state, ai)
            if not continue_execution:
                return False
        else:  # for loop completed without failure; return success
            return True


############################### Leaf Nodes ##################################
class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    def execute(self, state, ai):
        return self.check_function(state, ai)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.check_function.__name__


class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    def execute(self, state, ai):
        return self.action_function(state, ai)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.action_function.__name__
