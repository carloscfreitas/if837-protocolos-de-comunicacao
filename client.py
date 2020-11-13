from sevp import *

def main():
    csock = connect_to_server()
    csock.do_handshake()

    message = csock.rcv_encrypted_msn()
    print(message.code, message.data.decode('utf-8'))

    csock.send_encrypted_msn(201,
        b'A message from the Client verified for both integrity and authenticity')

if __name__ == "__main__":
    main()
