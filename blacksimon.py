# -*- coding: UTF-8 -*-
from irccrap import IRCBot, run_bot
import leSimon.Settings
import sys
import httplib2
import json
import urllib
import re
import requests
import sys
from random import choice
from subprocess import check_output
from leSimon.Asl import Asl
from leSimon.YT import Stats
from leSimon import Uptime
from leSimon.Told import Told
from leSimon import Modules
from leSimon.Slap import Slap

class GreeterBot(IRCBot):
    def uptime(self, nick, message, channel, _type='.', query=''):
        query = query.strip()
        if query == 'full':
            self.respond('%s' % (check_output("uptime")), channel, nick, _type)
        else:
            self.respond('%s' % (Uptime.uptime()), channel, nick, _type)

    def up(self, nick, message, channel, _type='.', query=''):
        query = query.strip()
        if query == '':
            self.respond('Please supply a URL.', channel, nick, comm=_type)
        else:
            html = requests.get("http://www.isup.me/{0}".format(query))
            if html.status_code == 200:
                html = re.sub("\t|\n", "", html.text)
                h = re.findall("<div id=\"container\">(.*?)<p>.*?</div>", html)[0]
                h = re.sub("<a href=\".*?\" class=\"domain\">", "", h)
                h = re.sub("</a>(:?</span>)?", "", h)
                h = re.sub("\s{2,}", " ", h).strip(" ")
                self.respond('\x02[ISUP]\x02 %s' % (h), channel, nick, _type)
            else:
                self.respond("I couldn't connect to isup.me :((", channel, nick, _type)

    def slap(self, nick, message, channel, _type='.', query=''):
        query = query.strip() or 'themself'
        self.respond('%s slaps %s around a bit with %s' % (nick, query, choice(Slap)), channel, nick, _type)

    def insult(self, nick, message, channel, _type='.', query=''):
        c = query.strip()
        html = requests.get("http://www.insultgenerator.org")
        if html.status_code == 200:
            html = re.sub("\t|\n", "", html.text)
            h = re.findall("<TD>(.*?)</TD>", html)[0]
            h = c + ': ' + h if c else h
            self.respond('%s' % h, channel, nick, _type)
        else:
            self.respond("I couldn't insult you.", channel, nick, _type)

    def oneliner(self, nick, message, channel, _type='.', query=''):
        html = requests.get("http://www.onelinerz.net/random-one-liners/1/")
        if html.status_code == 200:
            html = re.sub("\t|\n", "", html.text)
            h = re.findall(" class=\"oneliner\">(.*?)</div></td>", html)[0]
            self.respond('%s' % h, channel, nick, _type)
        else:
            self.respond("I couldn't make a oneliner.", channel, nick, _type)

    def youtube(self, nick, message, channel, _type='.', vidid=''):
        self.logger.debug('youtube found: %s' % channel)
        self.logger.debug('dev: %s' % dev)
        vidid = vidid.strip()
        if vidid:
            self.respond('%s' % Stats(message, dev), channel, nick, _type)

    def asl(self, nick, message, channel, _type='.'):
        genders = Asl.get('genders')
        agelist = Asl.get('ages')
        locations = Asl.get('locations')
        self.respond("{0}/{1}/{2}".format(choice(agelist), choice(genders), choice(locations)), channel, nick, _type)

    def told(self, nick, message, channel, _type='.'):
        self.respond("%s" % choice(Told), channel, nick, _type)

    def join_channel(self, nick, message, channel, _type='.', query=''):
        if nick not in GS['owners']:
            self.respond("You aren't in the bot operator list.", channel, nick, _type)
        else:
            query = query.strip()
            if query:
                self.join(query)

    def leave_channel(self, nick, message, channel, _type='.', query=''):
        if nick not in GS['owners']:
            self.respond("You aren't in the bot operator list.", channel, nick, _type)
        else:
            query = query.strip()
            if query:
                self.part(query)

    def say_channel(self, nick, message, channel, _type='.', chan='', text=''):
        if nick not in GS['owners']:
            self.respond("You aren't in the bot operator list.", channel, nick, _type)
        else:
            chan = chan.strip()
            text = text.strip()
            if chan and text:
                if chan[0] == '#':
                    self.respond(text, channel=chan)
                else:
                    self.respond(text, nick=chan)

    def command_patterns(self):
        return (
            self.ping('(?P<_type>[.@!])uptime(?P<query> full|)', self.uptime),
            self.ping('(?P<_type>[.@!])up(?P<query> .*|)', self.up),
            self.ping('(?P<_type>[.@!])slap(?P<query> .*|)', self.slap),
            self.ping('(?P<_type>[.@!])insult(?P<query> .*|)', self.insult),
            self.ping('(?P<_type>[.@!])oneliner', self.oneliner),
            self.ping('.*v=(?P<vidid>[a-zA-Z0-9_\-]{11}).*', self.youtube),
            self.ping('(?:\s+?|^)asl(?:\s+?|$)', self.asl),
            self.ping('(?:\s+?|^)[tT][oO][lL][dD](?:\s+?|$)', self.told),
            self.ping('(?P<_type>[.@!])join(?P<query> .*|)', self.join_channel),
            self.ping('(?P<_type>[.@!])leave(?P<query> .*|)', self.leave_channel),
            self.ping('(?P<_type>[.@!])say (?P<chan>.*|) (?P<text>.*|)', self.say_channel),
        )

try:
    if sys.argv[1] == 'dev':
        GS = leSimon.Settings.GS_dev
        dev = True
        print('dev mode.')
    else:
        GS = leSimon.Settings.GS
        dev = False
        print('normal mode.')
except:
    GS = leSimon.Settings.GS
    dev = False
    print('normal mode.')

host = GS['connect']['host']
port = GS['connect']['port']
nick = GS['connect']['nick']
channels = GS['connect']['channels'].split(',')

run_bot(GreeterBot, host, port, nick, channels)