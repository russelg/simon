def sendm(socket, msg, channel):
    message = 'PRIVMSG '+ channel + ' :' + msg + '\r\n'
    try:
        message = bytes(message, 'utf8')
    except:
        message = str(message).encode('utf8')
    socket.send(message)

def rawsend(socket, msg):
    try:
        message = bytes(msg,'utf8')
    except:
        message = str(msg).encode('utf8')
    socket.send(message)

def utf(data):
    try:
        return str(data, 'utf8')
    except:
        return data

def formathelp(msg):
    return msg.replace('<','\x02<').replace('>','>\x02').replace('[','\x02[').replace(']',']\x02')
