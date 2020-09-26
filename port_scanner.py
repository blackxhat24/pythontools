import sys
import getopt
import socket

HOST = ''
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT_FROM = 0
PORT_TO = 250

def getResultCode():
    global HOST, PORT_FROM, PORT_TO, SOCK
    for PORT in range(PORT_FROM,PORT_TO):
        res_code = SOCK.connect_ex((HOST, PORT))
        if res_code == 0:
            print(f'{HOST}:{PORT} is available')
        else:
            print(f'{HOST}:{PORT} is not available')

def main():
    global HOST, PORT_FROM, PORT_TO
    args, _ = getopt.getopt(sys.argv[1:], 'h:f:t:')
    for k, v in args:
        if k == '-h':
            HOST = v
        if k == '-f':
            PORT_FROM = int(v)
        if k == '-t':
            PORT_TO = int(v)
    getResultCode()

if __name__ == '__main__':
    main()

# reference doc
# https://docs.python.org/3/library/socket.html#timeouts-and-the-connect-method
