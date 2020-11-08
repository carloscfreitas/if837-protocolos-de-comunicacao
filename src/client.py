from sevp import *
import socket

def main():
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as s:
        while True:
            record = build_record(b'Hello, world')
            s.send(record)

            record = s.recv(RECORD_SIZE)
            data = dissect_record(record)
            print('Received', repr(data))

            ans = input('\nDo you want to continue? [y/N] ') 
            if ans == 'y':
                continue
            else: 
                break

if __name__ == "__main__":
    main()
