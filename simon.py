import json
import leSimon.Settings
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
from leSimon import Modules
from leSimon.Utils import sendm, rawsend, utf, formathelp

# this is python 3.1.5 compatible, dont bug me about newer/older versions

try:
    if sys.argv[1] == 'dev':
        GS = leSimon.Settings.GS_dev
        print('dev mode.')
    else:
        GS = leSimon.Settings.GS
        print('normal mode.')
except:
    GS = leSimon.Settings.GS
    print('normal mode.')

commands = {}

def Hook(plugin,find=False,help=[],operonly=False):
    try:
        nick = p.findall(ex[0])[0] or ''
    except:
        nick = ''
    if help != []:
        help1 = help[0]
        help2 = help[1]
        help2 = help[1]+' (operator only)' if operonly else help2
        commands[plugin] = [help1,help2]
    if find and plugin in GS['plugins']:
        print(plugin + ': ' + str(find) + '('+nick+', '+ex[2]+')')
        if operonly and nick not in GS['owners']:
            sendm(irc,nick + ": you're not on the operator list.", ex[2])
        else:
            print(' running: '+plugin)
            getattr(Modules, "%s" % plugin)(text, irc, ex, nick, commands)

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((GS['connect']['host'], GS['connect']['port']))

rawsend(irc,'USER '+ GS['connect']['username'] +' '+ GS['connect']['hostname'] +' '+ GS['connect']['servername'] +' :'+ GS['connect']['realname'] +'\n')
rawsend(irc,'NICK '+ GS['connect']['nick'] +'\n')
rawsend(irc,'PRIVMSG NickServ :IDENTIFY '+ GS['connect']['nickpass'] +'\n')
rawsend(irc,'JOIN '+ GS['connect']['channels'] +'\n')

while 1:
    text=irc.recv(2040)
    if not text:
        break

    text = utf(text)
    print(text)
    ex = text.split()
    p = re.compile('(?<=:)(.*?)(?=!)')
    print(p.findall(ex[0]))
    if p.findall(ex[0]):
        nick = p.findall(ex[0])[0]

    if p.findall(ex[0]):
        if ex[2] == GS['connect']['nick']:
            ex[2] = nick

    # if text.find(" JOIN :#") != -1 or text.find(" JOIN #") != -1 and text.find( GS['connect']['nick'] ) == -1 and ex[4].strip() != 'JOIN':
    #     if text.find(" JOIN #") != -1:
    #         sendm(irc, 'Hello ' + nick + ' :-) Welcome to ' + ex[2].strip() + '.', ex[2].strip())
    #     else:
    #         sendm(irc, 'Hello ' + nick + ' :-) Welcome to ' + ex[2].split(':')[1] + '.', ex[2].split(':')[1])

    Hook('PING', text.find('PING') != -1)
    Hook('help', text.find(":!help\r\n") != -1, ['', 'show this help message'])
    Hook('uptime', text.find(":!uptime\r\n") != -1 or text.find(":!uptime full\r\n") != -1, ['[full]', 'uptime for the server which leSimon is running on'])
    Hook('up', text.find(":!up ") != -1, ['<site>', 'checks if <site> is up'])
    Hook('slap', text.find(":!slap\r\n") != -1 or text.find(":!slap ") != -1, ['[user]', 'slaps [user] if given, else will slap the caller'])
    Hook('insult', text.find(":!insult\r\n") != -1 or text.find(":!insult ") != -1, ['[user]', 'displays an insult, hilights [user] if given'])
    Hook('oneliner', text.find(":!oneliner\r\n") != -1, ['', 'random edgy comment'])
    Hook('vidya', text.find(":!vidya\r\n") != -1, ['', 'generates a random name for a vidya gaem'])
    Hook('youtube', text.find("?v=") != -1)
    Hook('asl', text.find("asl") != -1)
    Hook('told', text.find("told") != -1)
    Hook('join', text.find(":!join #") != -1, ['<#channel>','makes bot join <#channel>'], operonly=True)
    Hook('leave', text.find(":!leave #") != -1, ['<#channel>','makes bot leave <#channel>'], operonly=True)
    Hook('quit', text.find(":!quit\r\n") != -1, ['','kill the bot'],operonly=True)
    Hook('saychat', text.find(":!saychat #") != -1, ['<#channel> <message>','say <message> to <#channel>'], operonly=True)