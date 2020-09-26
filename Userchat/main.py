# from human import Human

# h1 = Human('Rei',20)
# # print(h1.nama)
# # print(h1.umur)
# h2 = Human('Bambang',19)
# # print(h2.nama)
# # print(h2.umur)
import sys
"""
print(sys.argv[1:]) #python3 main.py lala lili lulu lolo
int main(char *argv, int **argv)
"""
import getopt
import socket
from threading import Thread
from userchat import Chat
import pickle

HOST = ""
PORT = 0
LISTEN = False
#klo UDP SOCK_DGRAM
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def victim_process(victim):
    while True:
        buffer = victim.recv(1024)
        chat = pickle.loads(buffer)
        print(f'From: {chat.name}')
        print(f'Message: {chat.message}')   

def attack():
    # print('Attacker')
    global SOCK, HOST, PORT
    print(HOST)
    input()
    SOCK.bind((HOST,PORT))
    SOCK.listen(5)
    #buat kalau gak langsung terminated
    while True:
        victim, _ = SOCK.accept()
        t = Thread(target=victim_process,args=(victim,))
        t.start()
        print(f'{HOST}:{PORT}')

def victim():
    # print('Victim')
    global SOCK, HOST, PORT
    SOCK.connect((HOST,PORT))
    while True:
        username = input('input username: ')
        message = input('input message: ')
        # perlu diencode karena message yang dikirim berupa byte 
        chat = Chat(username,message)
        buffer = pickle.dumps(chat)
        #hasil dari pickle gak perlu di encode
        SOCK.send(buffer)

def commend_attack():
    global LISTEN
    if LISTEN == True:
        attack()
    elif LISTEN == False:
        victim()

def main():
    global HOST, PORT, LISTEN
    """
        -v shortoption ":" = yang harus ada 
        --verbose long option "=" = yang harus ada
    """
    try:
        options, _ = getopt.getopt(sys.argv[1:],"h:p:",['host=','port='])
    except getopt.GetoptError as err:
        options, _ = getopt.getopt(sys.argv[1:],"p:l",['port=','listen'])
    for key, value in options:
        if key == '-h' or key == '--host':
            HOST = value
        if key == '-p' or key == '--port':
            PORT = int(value)
        if key == '-l' or key == '--listen':
            LISTEN = True
    # print(f'HOST {HOST} PORT {PORT}')
    # if LISTEN == True:
    #     print('Attacker')
    # else:
    #     print('Victim')
    commend_attack()
    input()
if __name__ == "__main__":
    main()