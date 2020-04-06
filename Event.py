import inspect
import os


class EventMode:
    PreHookMode = 0
    NormalHookMode = 1


class Event:
    instances = {}

    def cancel(self):
        pass

    def __init__(self, event_type: str, mode: EventMode):
        self.event_type = event_type
        self.func = None
        self.mode = mode

    def __call__(self, func):
        # noinspection PyTypeChecker
        self.__class__.instances[".".join(os.path.abspath(inspect.getfile(func)).split("__init__.py")[0].split('/')[-3:])[:-1]] = self
        self.func = func

    @classmethod
    def call(cls, event_type: str, mode: EventMode, obj):
        for k, v in cls.instances.items():
            if v.event_type == event_type:
                if v.mode == mode:
                    v.func(obj)

    @classmethod
    def unregister(cls,path):
        print(cls.instances)
        del cls.instances[path]
