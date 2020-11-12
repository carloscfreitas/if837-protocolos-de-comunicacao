from sevp import *

def main():
    csock = connect_to_server()

    # TODO Extract method "handshake"
    ### BEGIN OF HANDSHAKE
    cert = csock.get_server_cert()
    csock.check_certificate(cert)
    
    print(csock.server_cert)
    print(csock.server_pub_key)

    csock.send_client_public_key()
    
    message = csock.rcv_secret_key()
    print(message)
    ### END OF HANDSHAKE

if __name__ == "__main__":
    main()
