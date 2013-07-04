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
    # enabled plugins go below (only for normal simon, not blacksimon.)
    "plugins": [
        'PING',
        'help',
        'uptime',
        'up',
        'slap',
        'insult',
        'oneliner',
        'quit',
        'saychat',
        'join',
        'leave',
        'asl',
        'told',
        'youtube'
    ]
}