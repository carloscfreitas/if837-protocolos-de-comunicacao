from sevp import *

def main():
    csock = connect_to_server()
    csock.do_handshake()

    message = csock.rcv_encrypted_msn()
    while message.code != MESSAGE_CODE_END_SESSION:
        if message.code == MESSAGE_CODE_PROMPT:
            print(message.data.decode('utf-8'))
            option = input()
            csock.send_encrypted_msn(201, option.encode('utf-8'))
            message = csock.rcv_encrypted_msn()
    csock.close_connection()

if __name__ == "__main__":
    main()
