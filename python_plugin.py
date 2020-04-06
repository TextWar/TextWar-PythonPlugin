
import os
from Action import Action
from Command import Command
from Event import Event
from Event import EventMode
from py4j.java_gateway import JavaGateway, CallbackServerParameters
from onEnable import OnEnable, OnDisable
import importlib

PluginFolder = "./plugins"
MainModule = "__init__"
InfoFile = "/info.txt"

server = None

try:
    os.mkdir(PluginFolder)
except:
    pass





# noinspection PyMethodMayBeStatic
class PythonListener(object):

    def refreshPlugins(self):

        Plugin.refresh()
        for plugin in Plugin.plugins:
            Plugin.plugins[plugin].load()

    def loadPlugin(self, plugin: str):
        try:
            Plugin.plugins[plugin].load()
        except:
            Plugin.refresh()
            if Plugin.plugins[plugin].load() == 0:
                raise PythonPlugin("{} is not a directory or does not exist".format(plugin))

    def unloadPlugin(self, plugin: str):
        Plugin.plugins[plugin].unload()

    def reloadPlugin(self, plugin: str):
        Plugin.plugins[plugin].reload()

    def callEvent(self, name: str, mode: int, obj):
        event_mode = None
        if mode == 1:
            event_mode = EventMode.NormalHookMode
        if mode == 0:
            event_mode = EventMode.PreHookMode
        Event.call(name, event_mode, obj)

    def commandExecutor(self, name: str, args, player):
        Command.call(name, args, player)

    def getCommands(self):
        a = []
        for command in Command.instances:
            a.append(command.name)
        return a

    def getActions(self):
        a = []
        for action in Action.instances:
            a.append(action.name)
        return a

    def getServer(self, server_):
        global server
        server = server_

    def setPluginsDir(self, str):
        os.chdir(str)

    class Java:
        implements = ["cn.textwar.langs.python.PyPluginLoader"]


from py4j.java_gateway import JavaGateway, CallbackServerParameters

listener = PythonListener()
gateway = JavaGateway(
    callback_server_parameters=CallbackServerParameters(),
    python_server_entry_point=listener)
gateway.start_callback_server()


class PythonPlugin(Exception):
    pass


class Plugin:
    plugins = {}

    def __init__(self, path, info):
        self.__class__.plugins[path] = self
        self.path = path
        self.info = info
        self.enable = 0
        self.module = None

    def load(self):
        self.enable = 1
        if self.module is not None:
            self.module = importlib.reload(self.module)
        else:
            self.module = importlib.import_module(self.path)
        # except:
        #     return 0
        # finally:
        OnEnable.call(self.path)
        self.module.getServer(server)
        return self

    def unload(self):
        try:
            self.enable = 0
            OnDisable.call(self.path)
            Event.unregister(self.path)
        except:
            pass
        return self

    def info(self):
        return self.info

    def reload(self):
        # try:
        self.unload()
        self.module = importlib.reload(self.module)
        self.load()
        self.enable = 1
        # except:
        #     self.enable = 0
        return self

    def __repr__(self):
        return "".join(self.path.split(".")[1:])

    @classmethod
    def refresh(cls):
        possible_plugins = os.listdir(PluginFolder)
        for i in possible_plugins:
            location = os.path.join(PluginFolder, i)
            if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
                continue
            info = open(location + InfoFile, "r").read()
            cls(path=".".join(location.split("/")[1:]), info=info)
