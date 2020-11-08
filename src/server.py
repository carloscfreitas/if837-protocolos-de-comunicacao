from sevp import *
import socket
import _thread

def handle_client(conn, addr):
    """Trate de uma conexão (client) em particular."""
    while True:
        record = conn.recv(RECORD_SIZE)
        if not record:
            print('Bye', addr)
            break
        data = dissect_record(record)
        # reverse the given string
        data = data[0][::-1]

        record = build_record(data)
        conn.send(record)
    close_connection(conn)

def main():
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    while True:
        conn, addr = server.accept()
        print('Connected by', addr)
        _thread.start_new_thread(handle_client, (conn, addr))

if __name__ == "__main__":
    main()
