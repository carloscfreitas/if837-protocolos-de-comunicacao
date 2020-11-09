from cryptography.x509.oid import NameOID
from sevp import *

def main():
    conn = connect_to_server()
    while True:
        cert = conn.request_server_cert()
        conn.validate_certificate(cert)
        print(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME))

        ans = input('\nDo you want to send your public key? [y/N] ') 
        if ans == 'y':
            conn.send_client_public_key()
            continue
        else:
            break
    conn.close_connection()

if __name__ == "__main__":
    main()
