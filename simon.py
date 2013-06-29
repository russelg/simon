# this is python 3.1.5 compatible, dont bug me about newer/older versions
import json                             #for sorting through the Youtube API
from leSimon.Settings import GS, Locker         #Settings for the bot
import socket                           #for connecting to irc
import re                               #for regex
import requests                         #for scraping sites
import sys
from random import choice               #for random arrays
from subprocess import check_output     #for system commands
from leSimon.Asl import Asl             #Asl arrays
from leSimon.YT import YT, Stats        #Youtube functions
from leSimon import Uptime

def sendm(msg, channel): #sends message to <channel>
    # msg = msg.encode('utf-8')
    message = 'PRIVMSG '+ channel + ' :' + msg + '\r\n'
    try:
        message = bytes(message, 'utf8')
    except:
        message = str(message).encode('utf8')
    irc.send(message)

def rawsend(msg):
    try:
        message = bytes(msg,'utf8')
    except:
        message = str(msg).encode('utf8')
    irc.send(message)

def utf(data):
    try:
        return str(data, 'utf8')
    except:
        return data

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init. socket
irc.connect((GS['connect']['host'], GS['connect']['port'])) #connect to irc

#send irc data (user, nickname, nickserv identification, channels to join)
rawsend('USER '+ GS['connect']['username'] +' '+ GS['connect']['hostname'] +' '+ GS['connect']['servername'] +' :'+ GS['connect']['realname'] +'\n')
rawsend('NICK '+ GS['connect']['nick'] +'\n')
rawsend('PRIVMSG NickServ :IDENTIFY '+ GS['connect']['nickpass'] +'\n')
rawsend('JOIN '+ GS['connect']['channels'] +'\n')

Locker = Locker(10)

#start recieving irc data
while 1:
    text=irc.recv(2040)
    if not text:
        break

    text = utf(text)
    print(text)
    ex = text.split() #split the raw irc string at spaces (e.g ":russel!~russel@ara.ara PRIVMSG #tvfilm :hi\r\n")
    p = re.compile('(?<=:).*?(?=!)') #regex to grab the nickname (between the first : and !)
    if p.findall(ex[0]): #if we found their nick
        nick = p.findall(ex[0])[0] #grab users nick from raw irc

    if p.findall(ex[0]):
        if ex[2] == GS['connect']['nick']:
            ex[2] = nick

    if text.find('PING') != -1: #respond to server PINGs
        rawsend('PONG ' + text.split() [1] + '\r\n')

    if text.find(":!help\r\n") != -1: #send help about commands to the user via PM
        commands = {
            'uptime': 'uptime for the server which leSimon is running on',
            'up \x02<site>\x02': 'checks if \x02<site>\x02 is up',
            'slap \x02<user>\x02': 'slaps \x02<user>\x02',
            'insult \x02[user]\x02': 'displays an insult, hilights \x02[user]\x02 if given',
            'oneliner': 'random edgy comment',
            'vidya': 'generates a random name for a vidya gaem'
        }
        admin_commands = {
            'quit': 'r.i.p simon',
            'saychat \x02<#channel>\x02 \x02<message>\x02': 'say \x02<message>\x02 to \x02<#channel>\x02',
            'join \x02<#channel>\x02': 'join \x02<#channel>\x02',
            'leave \x02<#channel>\x02': 'leave \x02<#channel>\x02'
        }
        sendm( 'leSimon help docs or something, who cares' , nick )
        sendm( '<param> = necessary, [param] = optional' , nick )
        sendm( '\x02COMMANDS\x02' , nick )
        for key, value in list(commands.items()):
            sendm( '     !' + key + ' - ' + value, nick )
        if nick in GS['owners']:
            sendm( '\x02ADMIN/OP ONLY COMMANDS\x02' , nick )
            for key, value in list(admin_commands.items()):
                sendm( '     !' + key + ' - ' + value, nick )

    if text.find(" JOIN :#") != -1 and text.find( GS['connect']['nick'] ) == -1: #welcome a user to a channel (if the user isn't the bot)
        sendm( 'Hello ' + nick + '! Welcome to ' + ex[2].split(':')[1] + '.', ex[2].split(':')[1]  )

    if text.find(":!uptime\r\n") != -1 or text.find(":!uptime full\r\n") != -1: #grab uptime for server bot is running from
        if text.find(":!uptime full\r\n") != -1:
            sendm( utf(check_output("uptime")), ex[2] )
        else:
            sendm( utf(Uptime.uptime()), ex[2] )

    if text.find(":!4freedoms\r\n") != -1 or text.find(":!fourfreedoms\r\n") != -1 or text.find(":!fourrules\r\n") != -1: #muh freedums
        if Locker.IsLocked():
            sendm("Wait a bit longer, faggot.", nick)
        else:
            sendm( "ESSENTIAL FREEDOMS:", ex[2] )
            sendm( "     0: The freedom to run the program, for any purpose.", ex[2] )
            sendm( "     1: The freedom to study how the program works, and change it so it does your computing as you wish. Access to the source code is a precondition for this.", ex[2] )
            sendm( "     2: The freedom to redistribute copies so you can help your neighbor.", ex[2] )
            sendm( "     3: The freedom to distribute copies of your modified versions to others.  By doing this you can give the whole community a chance to benefit from your changes. Access to the source code is a precondition for this.", ex[2] )
            Locker.Lock()

    if text.find(":!up ") != -1: #query isup.me to see if a site is down for everyone or just you
        c = text.split(":!up ")[1].strip() #grab arguement for !up
        html = requests.get("http://www.isup.me/{0}".format(c)) #grab the info from #isup.me
        if html.status_code != 200: #is isup.me down??
            sendm( "I couldn't connect to isup.me :((", ex[2] )
        if html.status_code == 200: #no, it's not! continue...
            html = re.sub("\t|\n", "", html.text)
            h = re.findall("<div id=\"container\">(.*?)<p>.*?</div>", html)[0]
            h = re.sub("<a href=\".*?\" class=\"domain\">", "", h)
            h = re.sub("</a>(:?</span>)?", "", h)
            h = re.sub("\s{2,}", " ", h).strip(" ") #regex stuff ^
            sendm( "[ISUP] {0}".format(h), ex[2] )

    if text.find(":!slap\r\n") != -1 or text.find(":!slap ") != -1: #slap a user
        c = text.split(":!slap ")[1].strip() if text.find(":!slap ") != -1 else 'themself' #if the user didn't say who to slap, slap the person executing !slap
        s = open('leSimon/Fish.txt', 'r').readlines() #grab slap lines
        sendm( nick + ' slaps '+ c +' around a bit with ' + choice(s), ex[2] )

    if text.find(":!insult\r\n") != -1 or text.find(":!insult ") != -1: #insult a user
        c = text.split(":!insult ")[1].strip() if text.find(":!insult ") != -1 else ' ' #check if the user gave a name to insult, if they didn't: just show an insult.
        html = requests.get("http://www.insultgenerator.org") #grab the insult
        if html.status_code != 200: #is insultgenerator.org up?
            sendm( "I couldn't insult you :((", ex[2] )
        if html.status_code == 200: #yep, it's up.
            html = re.sub("\t|\n", "", html.text)
            h = re.findall("<TD>(.*?)</TD>", html)[0] #grab the insult
            h = c + ': ' + h if c != ' ' else h
            sendm( h, ex[2] )

    if text.find(":!oneliner\r\n") != -1: #say a one-liner
        html = requests.get("http://www.onelinerz.net/random-one-liners/1/") #grab one-liner
        if html.status_code != 200: #are they up?
            sendm( "I couldn't make a one-liner :((", ex[2] )
        if html.status_code == 200: #yep
            html = re.sub("\t|\n", "", html.text)
            h = re.findall(" class=\"oneliner\">(.*?)</div></td>", html)[0] #get the insult with regex
            sendm( h, ex[2] )

    if text.find(":!vidya\r\n") != -1: #make a random vidyagaem name
        html = requests.post("http://randomzoo.com/game/videogame-title.php", data={'a':'Generate+More'}) #grab the name
        if html.status_code != 200: #up?
            sendm( "I couldn't make a vidyagame title :((", ex[2] )
        if html.status_code == 200: #yep.
            html = re.sub("\t|\n", "", html.text)
            h = re.findall("<font id=result1>(.*?)</font>", html)[0] #regex bla
            sendm( h, ex[2] )

    if text.find("?v=") != -1: #do something when a youtube vid is said
        sendm( Stats(text), ex[2] )

    if text.find("asl") != -1: #asl??
        genders = Asl.get('genders')
        agelist = Asl.get('ages')
        locations = Asl.get('locations')
        sendm("{0}/{1}/{2}".format(choice(agelist), choice(genders), choice(locations)), ex[2])

    if text.find("told") != -1: #cash4told
        s = open('leSimon/Told.txt', 'r', encoding='utf-8').readlines() #grab slap lines
        sendm(choice(s), ex[2])

    if text.find(":!join ") != -1: #make bot join a channel
        c = text.split(":!join ")[1].strip()
        if nick in GS['owners']:
            rawsend('JOIN '+ c +'\r\n')
        else:
            sendm(nick + ': ur not le rassel or jff_', ex[2])

    if text.find(":!leave ") != -1: #make bot leave a channel
        c = text.split(":!leave ")[1].strip()
        if nick in GS['owners']:
            rawsend('PART '+ c +'\r\n')
        else:
            sendm(nick + ': ur not le rassel or jff_', ex[2])

    if text.find(":!quit\r\n") != -1: #make bot quit :((
        if nick in GS['owners']:
            sendm('see you, space cowboy', ex[2])
            rawsend('QUIT :h\r\n')
        else:
            sendm(nick + ': ur not le rassel or jff_', ex[2])

    if text.find(":!saychat ") != -1: #make bot say something to a channel
        message = re.findall(":!saychat\s(.+?)\s(.+)", text)
        if nick in GS['owners']:
            sendm(message[0][1], message[0][0])
        else:
            sendm(nick + ': ur not le rassel or jff_', ex[2])
