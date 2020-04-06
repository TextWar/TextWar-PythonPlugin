import inspect
import os


class Command:
    instances = {}

    def cancel(self):
        pass

    def __init__(self, name: str):
        self.name = name
        self.func = None

    def __call__(self, func):
        # noinspection PyTypeChecker
        self.__class__.instances[".".join(os.path.abspath(inspect.getfile(func)).split("__init__.py")[0].split('/')[-3:])[:-1]] = self
        self.func = func

    @classmethod
    def call(cls, name: str, args, player):
        for k, v in cls.instances.items():
            if v.name == name:
                v.func(args, player)

    @classmethod
    def unregister(cls,path):
        print(cls.instances)
        del cls.instances[path]
