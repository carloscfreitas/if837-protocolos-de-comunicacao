from sevp import *
import _thread

def handle_incoming_conn(ssock, addr):
    # TODO Extract method "handshake"
    ### BEGIN OF HANDSHAKE
    # TODO Use the message returned to validade the "client hello"
    message = ssock.rcv_client_hello()

    ssock.send_server_cert()
    ssock.rcv_client_public_key()
    print(ssock.client_pub_key)
    
    ssock.send_secret_key()
    print(ssock.secret_key)
    ### END OF HANDSHAKE

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
