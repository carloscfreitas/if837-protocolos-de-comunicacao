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

# SEVP Record
#   Byte order: Network (big-endian), "!"
#   Fields:
#       DLC (Data Length Code): 4-byte integer, "I"
#       DATA: 2048-byte string, "2048s"
RECORD_FMT = "!I2048s"
RECORD_SIZE = struct.calcsize(RECORD_FMT)

def init_server():
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    return SEVPSocket(server)

def connect_to_server():
    """Inicie uma conexão TCP com o servidor."""
    ssock = socket.create_connection((SERVER_HOST, SERVER_PORT))
    return SEVPSocket(ssock)

def read_cert_from_disk():
    with open("certs/certificate.pem", "rb") as cert_file:
        return cert_file.read()

def load_certificate(data):
    return x509.load_pem_x509_certificate(data)

def build_record(data):
    """Crie um record para ser enviado através do socket."""
    record_dlc = len(data)
    # Left justified version of the data
    data = data.ljust(2048, b'\x00')
    return struct.pack(RECORD_FMT, record_dlc, data)

def dissect_record(record):
    """Desempacote os campos de um record."""
    record_dlc, data = struct.unpack(RECORD_FMT, record)
    return data[:record_dlc]

class SEVPSocket():
    def __init__(self, socket):
        self.socket = socket
    
    def accept_incoming_conn(self):
        conn, addr = self.socket.accept()
        return SEVPSocket(conn), addr

    def send_certificate(self):
        cert_data = read_cert_from_disk()
        record = build_record(cert_data)
        self.socket.sendall(record)

    def close_connection(self):
        """Encerre a conexão."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def receive_record(self, size=RECORD_SIZE):
        return self.socket.recv(size)

    def request_server_cert(self):
        record = build_record(b'Client Hello')
        self.socket.sendall(record)

        record = self.socket.recv(RECORD_SIZE)
        data = dissect_record(record)
        return load_certificate(data)

    def validate_certificate(self, cert):
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
            self.close_connection()