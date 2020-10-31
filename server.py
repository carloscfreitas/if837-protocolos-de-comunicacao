import sevp
import socket
import _thread

def main():
    server = socket.create_server((sevp.SERVER_HOST, sevp.SERVER_PORT))
    while True:
        conn, addr = server.accept()
        print('Connected by', addr)
        _thread.start_new_thread(sevp.handle_client, (conn, addr))

if __name__ == "__main__":
    main()
