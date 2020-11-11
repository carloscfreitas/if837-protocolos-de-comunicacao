from sevp import *
import _thread

def handle_incoming_conn(server, addr):
    # TODO Use the data returned to validade the hello message
    data = server.rcv_client_hello()

    server.send_server_cert()
    server.rcv_client_public_key()
    print(server.client_pub_key)
    
    print('Bye', addr)
    server.close_connection()

def main():
    server = start_server()
    while True:
        conn, addr = server.accept_incoming_conn()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
