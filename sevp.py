# Secure Electronic Voting Protocol (SEVP)

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
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
    """Inicializa o servidor e retorna a instância SEVPSocket correspondente."""
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    return SEVPSocket(server)

def connect_to_server():
    """Faz uma tentativa de conexão TCP com o servidor e retorna a instância SEVPSocket correspondente."""
    ssock = socket.create_connection((SERVER_HOST, SERVER_PORT))
    return SEVPSocket(ssock)

def build_record(data):
    """Empacota dados num record SEVP para ser enviado pelo socket e retorna o record."""
    record_dlc = len(data)
    # Left justified version of the data
    data = data.ljust(2048, b'\x00')
    return struct.pack(RECORD_FMT, record_dlc, data)

def dissect_record(record):
    """Desempacota os campos de um record e retorna o dado em bytes."""
    record_dlc, data = struct.unpack(RECORD_FMT, record)
    return data[:record_dlc]

class SEVPSocket():
    def __init__(self, socket):
        """Inicializa o objeto com o socket passado no contrutor da classe."""
        self.socket = socket
    
    def accept_incoming_conn(self):
        """Habilita o servidor para aceitar uma conexão de chegada."""
        conn, addr = self.socket.accept()
        return SEVPSocket(conn), addr

    def send_certificate(self):
        """Efetua o envio do certificado do servidor."""
        with open("certs/certificate.pem", "rb") as cert_file:
            record = build_record(cert_file.read())
            self.socket.sendall(record)

    def close_connection(self):
        """Encerra a atual conexão."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def receive_record(self, size=RECORD_SIZE):
        """Aguarda recebimento de um record e o retorna."""
        return self.socket.recv(size)

    def request_server_cert(self):
        """Solicita ao servidor o envio do seu sertificado."""
        record = build_record(b'Client Hello')
        self.socket.sendall(record)

        record = self.socket.recv(RECORD_SIZE)
        data = dissect_record(record)
        return x509.load_pem_x509_certificate(data)

    def validate_certificate(self, cert):
        """Valida o certificado passado no argumento."""
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

    def send_client_public_key(self):
        """Envia a chave pública do cliente."""
        with open("certs/client_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=b"client",
            )

            public_key = private_key.public_key()
            pem = public_key.public_bytes(
               encoding=serialization.Encoding.PEM,
               format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            record = build_record(pem)
            self.socket.sendall(record)