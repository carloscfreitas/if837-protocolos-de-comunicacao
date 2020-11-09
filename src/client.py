from cryptography.x509.oid import NameOID
from sevp import *
import socket

def main():
    with connect_to_server() as s:
        while True:
            cert = request_server_cert(s)
            validate_certificate(cert, s)
            print(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME))

            ans = input('\nDo you want to continue? [y/N] ') 
            if ans == 'y':
                continue
            else: 
                break

if __name__ == "__main__":
    main()
