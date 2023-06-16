
class LaLaType:
    pass


class LaLaInt(LaLaType):
    def __init__(self, value: int):
        self.value = value


class LaLaBool(LaLaType):
    def __init__(self, value: bool):
        self.value = value


class LaLaString(LaLaType):
    def __init__(self, value):
        self.value = value


class LaLaSet(LaLaType):
    pass


class LaLaList(LaLaType):
    pass
