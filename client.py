from sevp import *

def main():
    csock = connect_to_server()
    csock.do_handshake()

    while True:
        message = csock.rcv_encrypted_msn()
        if message.code == MESSAGE_CODE_PROMPT:
            print(message.data.decode('utf-8'))
            user_input = input()
            csock.send_encrypted_msn(201, user_input.encode('utf-8'))
        elif message.code == MESSAGE_CODE_END_SESSION:
            print(message.data.decode('utf-8'))
            break
    csock.close_connection()

if __name__ == "__main__":
    main()
