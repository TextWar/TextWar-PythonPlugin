from __future__ import print_function

from Event import Event, EventMode
from onEnable import OnEnable, OnDisable

Server = None


def print(*args, **kwargs):
    Server.getLogger().info(str(*args) + str(**kwargs))


@Event("PlayerMoveEvent", EventMode.NormalHookMode)
def event(obj):
    print("Player move!")


def getServer(server):
    global Server
    Server = server


@OnEnable()
def onEnable():
    print("Example plugin load!")


@OnDisable()
def onDisable():
    print("Example plugin unload!")
