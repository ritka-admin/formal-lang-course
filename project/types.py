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


class LaLaSet(LaLaType):
    def __init__(self, value: set):
        self.value = value


class LaLaList(LaLaType):
    def __init__(self, value: list):
        self.value = value


class LaLaFa(LaLaType):
    def __init__(self, value: EpsilonNFA):
        self.value = value
