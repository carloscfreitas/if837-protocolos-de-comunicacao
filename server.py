from sevp import *
import socket
import _thread

def main():
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    while True:
        conn, addr = server.accept()
        print('Connected by', addr)
        _thread.start_new_thread(handle_client, (conn, addr))

if __name__ == "__main__":
    main()
