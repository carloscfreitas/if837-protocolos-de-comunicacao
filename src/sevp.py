# Secure Electronic Voting Protocol

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

def build_record(data):
    """Crie um record para ser enviado através do socket."""
    return struct.pack(RECORD_FMT, data)

def dissect_record(record):
    """Desempacote os campos de um record."""
    data = struct.unpack(RECORD_FMT, record)
    return data
