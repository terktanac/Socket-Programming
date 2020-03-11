# import socket programming library 
import socket 
from _thread import *
import threading 
import random

print_lock = threading.Lock() 
users = {}
players = []
maxPlayers = 2
numPlayers = 0
lastNumber = 0
roundNumber = 0

def joining_gane(c):
    global numPlayers, maxPlayers, roundNumber
    if numPlayers < maxPlayers:
        numPlayers += 1
        players.append(c)
        out = '### ' + users[c] + ' is joining counting game ###'
        send_to_all(out)
        if numPlayers == maxPlayers:
            roundNumber = random.randint(0,1)
            send_to_all("""### Let's play the counting game.
### In this game, we can count at most three numbers per turn.
### the first player who have to count number 20 will win!""")
            send_to_all("### Let's start! " + users[players[roundNumber]] +" go first. (e.g. 1 2 3)\n")
    else:
        c.send('The room is full!'.encode('utf-8'))

def check_winner(c):
    global numPlayers, lastNumber, players
    send_to_all(users[c] + ' is the Winner. Thank you for playing.')
    numPlayers = 0
    lastNumber = 0
    players = []

def counting_game(c,rawData):
    global lastNumber
    if not check_input(c,rawData):
        return
    out = users[c] + ': ' + rawData.decode('utf-8')
    print(out)
    send_to_all(out)
    data = [int(e) for e in rawData.split()]
    lastNumber = max(data)
    if lastNumber >= 20:
        check_winner(c)


def check_input(c,rawData):
    global lastNumber, roundNumber
    if players[roundNumber] != c:
        c.send("It's not your turn.".encode('utf-8'))
        return False
    stringData = rawData.decode('utf-8')
    for i in stringData.split():
        try:
            int(i)
        except ValueError:
            c.send("You have to enter a number! Please enter agian.".encode('utf-8'))
            return False
    data = [int(e) for e in stringData.split()]
    for i in range(len(data)-1):
        if(data[i] + 1!= data[i+1]):
            c.send("You have to enter a sequence number! Please enter agian.".encode('utf-8'))
            return False
    if(len(data) > 3):
        c.send("Too much number! Please enter agian.".encode('utf-8'))
        return False
    if(min(data) != lastNumber + 1 and lastNumber != 0):
        c.send("You have to continue from other player! Please enter agian.".encode('utf-8'))
        return False
    if(min(data) != lastNumber + 1 and lastNumber == 0):
        c.send("You have to start from 1! Please enter agian.".encode('utf-8'))
        return False
    if roundNumber == 0:
        roundNumber = 1
    else:
        roundNumber = 0
    return True
    
def send_to_all(message):
    for conn in users:
        conn.send(message.encode('utf-8'))

def new_client(c):
    global numPlayers, maxPlayers
    name = c.recv(1024).decode('utf-8')
    greet = 'Welcome ' + name
    c.send(greet.encode('utf-8'))
    users[c] = name
    while True: 
        data = c.recv(1024)
        if not data: 
            print('Bye') 
            print_lock.release() 
            break

        if c in players and numPlayers == 2:
            counting_game(c,data)
        else:
            out = users[c] + ': ' + data.decode('utf-8')
            print(out)
            send_to_all(out)

            if data.decode('utf-8') == 'start':
                joining_gane(c)
    c.close() 
  
  
def Main(): 
    host = "" 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
    s.listen(5) 
    print("socket is listening")  
    while True: 
        c, addr = s.accept() 
        print('Connected to :',addr[0], addr[1]) 
        start_new_thread(new_client, (c, )) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 