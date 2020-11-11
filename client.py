from sevp import *

def main():
    conn = connect_to_server()

    cert = conn.get_server_cert()
    conn.check_certificate(cert)
    print(cert)

    conn.send_client_public_key()

if __name__ == "__main__":
    main()
