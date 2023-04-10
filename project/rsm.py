from project.ecfg import ECFG


class Box:
    """
    This class represents a box for recursive state machine
    """

    def __init__(self, variable=None, dfa=None):
        self.dfa = dfa
        self.variable = variable

    def minimize(self):
        """
        Minimize dfa in the given Box
        """
        self.dfa = self.dfa.minimize()


class RSM:
    """
    This class represents a recursive state machine (RSM).
    """

    def __init__(self, start_symbol, boxes):
        self.start_symbol = start_symbol
        self.boxes = boxes

    def minimize(self):
        for box in self.boxes:
            box.minimize()
        return self

    @staticmethod
    def ecfg_to_rsm(ecfg: ECFG):
        """
        Create RSM for the provided ECFG

        Parameters:
            ecfg: extended context-free grammar

        Returns:
            Recursive state machine for the provided ECFG
        """
        boxes = {}
        for variable, regex in ecfg.productions.items():
            boxes[variable] = regex.to_epsilon_nfa()

        return RSM(ecfg.start_symbol, boxes)
