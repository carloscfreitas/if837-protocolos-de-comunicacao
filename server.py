from sevp import *
import _thread

def handle_incoming_conn(conn, addr):
    while True:
        data = conn.rcv_client_hello()
        if not data:
            print('Bye', addr)
            break

        conn.send_server_cert()
        client_key = conn.rcv_client_public_key()
        print(client_key)

    conn.close_connection()

def main():
    server = init_server()
    while True:
        conn, addr = server.accept_incoming_conn()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
