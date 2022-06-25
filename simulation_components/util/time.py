from simulation_components.util.singleton import Singleton


class Time(metaclass=Singleton):
    _value: float
    _base: int
    _res: float

    def __init__(self, base: int):
        self._value = 0.0
        self._base = base
        self._res = 24 * 60 * 60 / base

    def tick(self):
        self._value += 1
        self._value %= self._base

    def time_sec(self):
        return self._value * self._res

    def __float__(self):
        return self._value

    def __str__(self):
        _time = self.time_sec()
        return f'{int(_time / (60 * 60) % 24):0>2}:{int(_time / 60) % 60:0>2}.{int(_time % 60)}'

    @staticmethod
    def str2sec(time_str: str):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, [int(i) for i in time_str.split(":")])])
