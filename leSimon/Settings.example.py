import json
from threading import Timer
from time import strftime

GS = { #Settings array
    "connect": {
        "host": "irc.rizon.net", #irc server hostname
        "port": 6667, #irc port
        "nick": "NICKNAME", #bot nickname
        "username": "USERNAME", #bot username
        "hostname": "example.com", #bot hostname
        "servername": "example.com", #bot servername
        "realname": "real name here", #bots real name
        "nickpass": "nickserv pass", #password for NickServ
        "channels": "channels" #channels to join, comma seperated
    },

    #irc ids of people that can use the bot admin commands
    "owners": [
        'user1',
        'user2'
    ],

    "botIdent": "botidenthere"
}

class Locker(object):
    def __init__(self, Time=None):
        self.Time = Time if Time or Time == 0 and type(Time) == int else 10
        # banhammer would be proud ;-;
        self.Locked = False

    def Lock(self):
        if not self.Locked:
            if self.Time > 0:
                self.Locked = True
                t = Timer(self.Time, self.Unlock, ())
                t.daemon = True
                t.start()
        return self.Locked

    def IsLocked(self):
        return self.Locked

    def Unlock(self):
        self.Locked = False
        return self.Locked