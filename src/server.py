from sevp import *
import socket
import _thread

def handle_incoming_conn(conn, addr):
    while True:
        record = conn.recv(RECORD_SIZE)
        if not record:
            print('Bye', addr)
            break
        send_certificate(conn)
    close_connection(conn)

def main():
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    while True:
        conn, addr = server.accept()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
