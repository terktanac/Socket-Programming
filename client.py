# Import socket module 
import sys
import socket 
from _thread import *
import threading
  
def client_send(socket):
    while True:
        try:
            message = input()
            sys.stdout.write("\x1b[1A\x1b[2K")
            socket.send(message.encode('utf-8')) 
        except:
            print("error from send")
            socket.close()
            return

def client_receive(socket):
    while True:
        try:
            print(socket.recv(1024).decode("utf-8"))
        except:
            print("error from receive")
            socket.close()
            return

def Main(): 
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.connect((host,port)) 
    name = input('\nPlease Enter Your Name: ') 
    sys.stdout.write("\x1b[1A\x1b[2K")
    s.send(name.strip().encode('utf-8')) 
    send = threading.Thread(target=client_send, args=(s,))
    send.start()
    receive = threading.Thread(target=client_receive, args=(s,))
    receive.start() 
  
if __name__ == '__main__': 
    Main()