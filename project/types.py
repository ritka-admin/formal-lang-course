from pyformlang.finite_automaton import EpsilonNFA


class LaLaType:
    pass


class LaLaInt(LaLaType):
    def __init__(self, value: int):
        self.value = value


class LaLaBool(LaLaType):
    def __init__(self, value: bool):
        self.value = value


class LaLaString(LaLaType):
    def __init__(self, value: str):
        self.value = value
        self.value = self.value.replace('\"', '')


class LaLaCollection(LaLaType):
    pass


class LaLaSet(LaLaCollection):
    def __init__(self, value: set):
        self.value = value


class LaLaList(LaLaCollection):
    def __init__(self, value: list):
        self.value = value


class LaLaFa(LaLaType):
    def __init__(self, value: EpsilonNFA):
        self.value = value


class LaLaLambda(LaLaType):
    def __init__(self, args: list, body):
        self.args = args
        self.body = body
