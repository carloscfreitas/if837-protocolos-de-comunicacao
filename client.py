from sevp import *

def main():
    csock = connect_to_server()

    cert = csock.get_server_cert()
    csock.check_certificate(cert)
    
    print(csock.server_cert)
    print(csock.server_pub_key)

    csock.send_client_public_key()
    
    message = csock.rcv_secret_key()
    print(message)

if __name__ == "__main__":
    main()
