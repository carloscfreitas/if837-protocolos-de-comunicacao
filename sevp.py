# Secure Eletronic Voting Protocol

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

import cryptography
import socket
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 50008

RECORD_FMT = "!12s"     # A single 12-byte string in network byte order (big-endian)
RECORD_SIZE = struct.calcsize(RECORD_FMT)

def connect_to_server(): 
    """Inicie uma conexão TCP com o servidor."""
    pass

def check_certificate():
    """Valide o certificado recebido do servidor."""
    pass

def close_connection(conn):
    """Encerre a conexão."""
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def handle_client(conn, addr):
    """Trate de uma conexão (client) em particular."""
    while True:
        record = conn.recv(RECORD_SIZE)
        if not record:
            print('Bye', addr)
            break
        data = dissect_record(record)
        # reverse the given string
        data = data[0][::-1]

        record = build_record(data)
        conn.send(record)
    close_connection(conn)

def build_record(data):
    """Crie um record para ser enviado através do socket."""
    return struct.pack(RECORD_FMT, data)

def dissect_record(record):
    """Desempacote os campos de um record."""
    data = struct.unpack(RECORD_FMT, record)
    return data
