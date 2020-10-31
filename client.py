import sevp
import socket

def main():
    with socket.create_connection(
        (sevp.SERVER_HOST, sevp.SERVER_PORT)) as s:
        while True:
            s.sendall(b'Hello, world')

            data = s.recv(1024)
            print('Received', repr(data))

            ans = input('\nDo you want to continue? [Y/n] ') 
            if ans == 'y':
                continue
            else: 
                break

if __name__ == "__main__":
    main()
