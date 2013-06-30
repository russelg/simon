import json
import socket
import re
import requests
import sys
from random import choice
from subprocess import check_output
from leSimon.Asl import Asl
from leSimon.YT import Stats
from leSimon import Uptime
from leSimon.Told import Told
from leSimon.Utils import sendm, rawsend, utf, formathelp
from leSimon.Slap import Slap
from leSimon.Settings import GS

def help(text, irc, ex, nick, commands):
    sendm(irc, 'leSimon help docs or something, who cares' , nick )
    sendm(irc, formathelp('<param> = necessary, [param] = optional') , nick )
    sendm(irc, '\x02COMMANDS\x02' , nick )
    for key, value in list(commands.items()):
        if key in GS['plugins']:
            if value[0] != '':
                args = ' ' + formathelp(value[0])
            else:
                args = ''
            msgs = formathelp(value[1])
            sendm(irc, '     !' + key + args + ' - ' + msgs, nick )

def uptime(text, irc, ex, nick, commands):
    if text.find(":!uptime full\r\n") != -1:
        sendm(irc, utf(check_output("uptime")), ex[2] )
    else:
        sendm(irc, utf(Uptime.uptime()), ex[2] )

def up(text, irc, ex, nick, commands):
    c = text.split(":!up ")[1].strip()
    html = requests.get("http://www.isup.me/{0}".format(c))
    if html.status_code != 200:
        sendm(irc, "I couldn't connect to isup.me :((", ex[2] )
    if html.status_code == 200:
        html = re.sub("\t|\n", "", html.text)
        h = re.findall("<div id=\"container\">(.*?)<p>.*?</div>", html)[0]
        h = re.sub("<a href=\".*?\" class=\"domain\">", "", h)
        h = re.sub("</a>(:?</span>)?", "", h)
        h = re.sub("\s{2,}", " ", h).strip(" ")
        sendm(irc, "[ISUP] {0}".format(h), ex[2] )

def slap(text, irc, ex, nick, commands):
    c = text.split(":!slap ")[1].strip() if text.find(":!slap ") != -1 else 'themself'
    sendm(irc, nick + ' slaps '+ c +' around a bit with ' + choice(Slap), ex[2] )

def insult(text, irc, ex, nick, commands):
    print('run insult')
    c = text.split(":!insult ")[1].strip() if text.find(":!insult ") != -1 else ' '
    # c = match.group(1).strip() if match.group(1) else ' '
    html = requests.get("http://www.insultgenerator.org")
    if html.status_code != 200:
        sendm(irc, "I couldn't insult you :((", ex[2] )
    if html.status_code == 200:
        html = re.sub("\t|\n", "", html.text)
        h = re.findall("<TD>(.*?)</TD>", html)[0]
        h = c + ': ' + h if c != ' ' else h
        print('sending')
        sendm(irc, h, ex[2] )

def oneliner(text, irc, ex, nick, commands):
    html = requests.get("http://www.onelinerz.net/random-one-liners/1/")
    if html.status_code != 200:
        sendm(irc, "I couldn't make a one-liner :((", ex[2] )
    if html.status_code == 200:
        html = re.sub("\t|\n", "", html.text)
        h = re.findall(" class=\"oneliner\">(.*?)</div></td>", html)[0]
        sendm(irc, h, ex[2] )

def vidya(text, irc, ex, nick, commands):
    html = requests.post("http://randomzoo.com/game/videogame-title.php", data={'a':'Generate+More'})
    if html.status_code != 200:
        sendm(irc, "I couldn't make a vidyagame title :((", ex[2] )
    if html.status_code == 200:
        html = re.sub("\t|\n", "", html.text)
        h = re.findall("<font id=result1>(.*?)</font>", html)[0]
        sendm(irc, h, ex[2] )

def youtube(text, irc, ex, nick, commands):
    sendm(irc, Stats(text), ex[2] )

def asl(text, irc, ex, nick, commands):
    genders = Asl.get('genders')
    agelist = Asl.get('ages')
    locations = Asl.get('locations')
    sendm(irc,"{0}/{1}/{2}".format(choice(agelist), choice(genders), choice(locations)), ex[2])

def told(text, irc, ex, nick, commands):
    sendm(irc,choice(Told), ex[2])

def join(text, irc, ex, nick, commands):
    c = text.split(":!join ")[1].strip()
    rawsend(irc,'JOIN '+ c +'\r\n')

def leave(text, irc, ex, nick, commands):
    c = text.split(":!leave ")[1].strip()
    rawsend(irc,'PART '+ c +'\r\n')

def quit(text, irc, ex, nick, commands):
    sendm(irc,'see you, space cowboy', ex[2])
    rawsend(irc,'QUIT :h\r\n')
    exit()

def saychat(text, irc, ex, nick, commands):
    message = re.findall(":!saychat\s(.+?)\s(.+)", text)
    sendm(irc,message[0][1], message[0][0])

def PING(text, irc, ex, nick, commands):
    rawsend(irc,'PONG ' + text.split()[1] + '\r\n')