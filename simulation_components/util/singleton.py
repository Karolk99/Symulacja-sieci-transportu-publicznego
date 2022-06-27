import abc


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        cls.__ext_name__ = cls.__name__
        return cls._instances[cls]

    def force_remove_instance(self) -> None:
        self._instances = {k: v for k, v in self._instances.items() if k.__name__ != self.__name__}

    @classmethod
    def is_instance(mcs, name: object = None) -> bool:
        if not name:
            name = mcs.__class__
        return name in mcs._instances
