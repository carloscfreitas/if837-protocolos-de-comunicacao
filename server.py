from sevp import *
import _thread

def handle_incoming_conn(ssock, addr):
    # TODO Use the data returned to validade the hello message
    data = ssock.rcv_client_hello()

    ssock.send_server_cert()
    ssock.rcv_client_public_key()
    print(ssock.client_pub_key)
    
    ssock.send_secret_key()
    print(ssock.secret_key)

    print('Bye', addr)
    ssock.close_connection()

def main():
    ssock = start_server()
    while True:
        conn, addr = ssock.accept_incoming_conn()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
