import inspect
import os


class OnEnable:
    instances = {}

    def __init__(self):
        self.func = None

    def __call__(self, func):
        self.__class__.instances[".".join(os.path.abspath(inspect.getfile(func)).split("__init__.py")[0].split('/')[-3:])[:-1]] = self
        self.func = func

    @classmethod
    def call(cls, plugin):
        try:
            cls.instances[plugin].func()
        except:
            pass


class OnDisable:
    instances = {}

    def __init__(self):
        self.func = None

    def __call__(self, func):
        # noinspection PyTypeChecker
        self.__class__.instances[".".join(os.path.abspath(inspect.getfile(func)).split("__init__.py")[0].split('/')[-3:])[:-1]] = self
        self.func = func

    @classmethod
    def call(cls, plugin):
        try:
            cls.instances[plugin].func()
        except:
            pass
