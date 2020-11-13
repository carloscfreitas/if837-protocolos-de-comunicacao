from sevp import *
import _thread

def handle_incoming_conn(ssock, addr):
    ssock.do_handshake()

    ssock.send_encrypted_msn(200,
        b'A message from the Server verified for both integrity and authenticity\nAnother line...')

    message = ssock.rcv_encrypted_msn()
    print(message.code, message.data)

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
