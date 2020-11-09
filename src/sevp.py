# Secure Electronic Voting Protocol

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
import socket
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 50008

RECORD_FMT = "!1273s"     # A single 1273-byte string in network byte order (big-endian)
RECORD_SIZE = struct.calcsize(RECORD_FMT)

def connect_to_server(): 
    """Inicie uma conexão TCP com o servidor."""
    return socket.create_connection((SERVER_HOST, SERVER_PORT))

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

def send_certificate(conn):
    cert_data = read_cert_from_disk()
    record = build_record(cert_data)
    conn.send(record)

def read_cert_from_disk():
    with open("certs/certificate.pem", "rb") as cert_file:
        return cert_file.read()

def load_certificate(data):
    return x509.load_pem_x509_certificate(data)

def request_server_cert(s):
    record = build_record(b'Hello, world')
    s.send(record)

    record = s.recv(RECORD_SIZE)
    data = dissect_record(record)

    return load_certificate(data[0])

def validate_certificate(cert, s):
    issuer_public_key = cert.public_key()
    try:
        issuer_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            # Depends on the algorithm used to create the certificate
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
    except InvalidSignature:
        close_connection(s)