from sevp import *
import pprint
import _thread

def handle_incoming_conn(conn, addr):
    while True:
        record = conn.receive_record()
        if not record:
            print('Bye', addr)
            break
        conn.send_certificate()

        record_key = conn.receive_record()
        if not record_key:
            print('Bye', addr)
            break
        client_key = dissect_record(record_key)
        pprint.pprint(client_key)

    conn.close_connection()

def main():
    server = init_server()
    while True:
        conn, addr = server.accept_incoming_conn()
        print('Connected by', addr)
        _thread.start_new_thread(handle_incoming_conn, (conn, addr))

if __name__ == "__main__":
    main()
