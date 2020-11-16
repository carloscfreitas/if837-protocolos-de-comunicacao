from db import *
from sevp import *
import _thread

def handle_incoming_conn(ssock, addr):
    ssock.do_handshake()

    ssock.send_encrypted_msn(MESSAGE_CODE_PROMPT,
        b'***Eletronic Voting 2020.3***\n\nPlease, enter your credentials <login,password>:')

    message = ssock.rcv_encrypted_msn()
    credentials = message.data.decode('utf-8')
    login, pwd = credentials.split(',')
    if is_user_registered(login, pwd):
        candidates_menu = get_candidates_str()
        ssock.send_encrypted_msn(MESSAGE_CODE_PROMPT, candidates_menu.encode('utf-8'))
        message = ssock.rcv_encrypted_msn()
        print(addr, message.data)

    print('Bye', addr)
    ssock.send_encrypted_msn(MESSAGE_CODE_END_SESSION, b'Bye')
    ssock.close_connection()

def main():
    ssock = start_server()
    while True:
        conn, addr = ssock.accept_incoming_conn()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
