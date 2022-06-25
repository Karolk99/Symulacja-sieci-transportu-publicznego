class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def force_remove_instance(cls) -> None:
        # TODO fix me
        cls._instances = {}

    @classmethod
    def is_instance(mcs) -> bool:
        return mcs.__class__ in mcs._instances
