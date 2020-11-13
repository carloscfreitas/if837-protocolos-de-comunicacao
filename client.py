from sevp import *

def main():
    csock = connect_to_server()

    # TODO Extract method "handshake"
    ### BEGIN OF HANDSHAKE
    cert = csock.get_server_cert()
    csock.check_certificate(cert)
    csock.send_client_public_key()
    csock.rcv_secret_key()
    ### END OF HANDSHAKE

    message = csock.rcv_encrypted_msn()
    print(message.code, message.data.decode('utf-8'))

    csock.send_encrypted_msn(201,
        b'A message from the Client verified for both integrity and authenticity')

if __name__ == "__main__":
    main()
