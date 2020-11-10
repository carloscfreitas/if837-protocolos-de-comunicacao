from sevp import *

def main():
    conn = connect_to_server()
    while True:
        cert = conn.get_server_cert()
        conn.check_certificate(cert)
        print(cert)

        conn.send_client_public_key()

        ans = input('\nDo you want to repeat? [y/N] ') 
        if ans == 'y':    
            continue
        else:
            break
    conn.close_connection()

if __name__ == "__main__":
    main()
