# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:06:41 2016

@author: Sup
"""

from twisted.spread import pb
from twisted.internet import reactor
from zope.interface import implements
from twisted.cred import checkers, portal

class MyPerspective(pb.Avatar):
    def __init__(self, name):
        self.name = name
    def perspective_foo(self, arg):
        print "I am", self.name, "perspective_foo(",arg,") called on", self

class MyRealm:
    implements(portal.IRealm)
    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        return pb.IPerspective, MyPerspective(avatarId), lambda:None

p = portal.Portal(MyRealm())
c = checkers.InMemoryUsernamePasswordDatabaseDontUse(user1="pass1",
                                                     user2="pass2")
p.registerChecker(c)
reactor.listenTCP(8800, pb.PBServerFactory(p))
reactor.run()