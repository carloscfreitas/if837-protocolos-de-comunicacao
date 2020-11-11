# Secure Electronic Voting Protocol (SEVP)

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import NameOID
import os
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

CERT_COMMON_NAME = 'electronicvoting.com'

CLIENT_PVT_KEY_PATH = "certs/client_key.pem"
CLIENT_PVT_KEY_PWD = b"client"
SERVER_PVT_KEY_PATH = "certs/server_key.pem"
SERVER_PVT_KEY_PWD = b"server"
SERVER_CERT_PATH = "certs/certificate.pem"

def start_server():
    """Inicializa o servidor e retorna uma instância de ServerSocket."""
    sock = socket.create_server((SERVER_HOST, SERVER_PORT))
    return ServerSocket(sock)

def connect_to_server():
    """Faz uma tentativa de conexão TCP com o servidor e retorna um instância de ClientSocket."""
    sock = socket.create_connection((SERVER_HOST, SERVER_PORT))
    return ClientSocket(sock)

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

def load_private_key(path, password):
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=password)

def load_certificate(path):
    with open(path, "rb") as cert_file:
        return x509.load_pem_x509_certificate(cert_file.read())

class SEVPSocket():
    def __init__(self, socket):
        """Inicializa o objeto com o socket passado no contrutor da classe."""
        self.socket = socket
    
    def send_data(self, data):
        """Constrói um record a partir de dados e envia ele pelo socket."""
        record = build_record(data)
        self.socket.sendall(record)

    def receive_data(self):
        """Recebe um record pelo socket, desempacota o record e retorna os dados."""
        record = self.socket.recv(RECORD_SIZE)
        return dissect_record(record)

    def send_encrypted_msn(self, message, public_key):
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.send_data(ciphertext)

    def rcv_encrypted_msn(self, private_key):
        ciphertext = self.receive_data()
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def close_connection(self):
        """Encerra a conexão atual."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

class ClientSocket(SEVPSocket):
    def __init__(self, socket):
        super().__init__(socket)
        self.server_cert = None
        self.server_pub_key = None
        self.client_prv_key = load_private_key(CLIENT_PVT_KEY_PATH, CLIENT_PVT_KEY_PWD)
        self.client_pub_key = self.client_prv_key.public_key()
        self.secret_key = None

    def get_server_cert(self):
        """Solicita o certificado ao servidor e retorna uma instância de Certificate."""
        self.send_data(b'Client Hello')
        cert_data = self.receive_data()
        self.server_cert = x509.load_pem_x509_certificate(cert_data)
        self.server_pub_key = self.server_cert.public_key()
        return self.server_cert
    
    def check_certificate(self, cert):
        """Valida o certificado passado no argumento."""
        common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if common_name != CERT_COMMON_NAME:
            self.close_connection()
            return False

        issuer_public_key = self.server_pub_key
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
        pem = self.client_pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.send_data(pem)
    
    def rcv_secret_key(self):
        self.secret_key = super().rcv_encrypted_msn(self.client_prv_key)
        return self.secret_key

class ServerSocket(SEVPSocket):
    def __init__(self, socket):
        super().__init__(socket)
        self.server_cert = load_certificate(SERVER_CERT_PATH)
        self.server_pub_key = self.server_cert.public_key()
        self.server_prv_key = load_private_key(SERVER_PVT_KEY_PATH, SERVER_PVT_KEY_PWD)
        self.client_pub_key = None
        self.secret_key = None
    
    def accept_incoming_conn(self):
        """Habilita o servidor para aceitar uma conexão de chegada."""
        conn, addr = self.socket.accept()
        return ServerSocket(conn), addr

    def send_server_cert(self):
        """Efetua o envio do certificado do servidor."""
        cert_data = self.server_cert.public_bytes(serialization.Encoding.PEM)
        self.send_data(cert_data)

    def rcv_client_hello(self):
        """Recebe a mensagem "client hello" e retorna os dados da mensagem."""
        return self.receive_data()
    
    def rcv_client_public_key(self):
        """Recebe a chave pública do cliente e retorna uma instância de RSAPublicKey."""
        key_data = self.receive_data()
        self.client_pub_key = serialization.load_pem_public_key(key_data)
        return self.client_pub_key
    
    def send_secret_key(self):
        self.secret_key = os.urandom(32)
        super().send_encrypted_msn(self.secret_key, self.client_pub_key)