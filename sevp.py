# Secure Electronic Voting Protocol (SEVP)

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import NameOID
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

def init_server():
    """Inicializa o servidor e retorna uma instância de SEVPSocket."""
    server = socket.create_server((SERVER_HOST, SERVER_PORT))
    return SEVPSocket(server)

def connect_to_server():
    """Faz uma tentativa de conexão TCP com o servidor e retorna um instância de SEVPSocket."""
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
        self.__socket = socket
    
    def accept_incoming_conn(self):
        """Habilita o servidor para aceitar uma conexão de chegada."""
        conn, addr = self.__socket.accept()
        return SEVPSocket(conn), addr

    def send_server_cert(self):
        """Efetua o envio do certificado do servidor."""
        with open("certs/certificate.pem", "rb") as cert_file:
            self.__send_data(cert_file.read())

    def close_connection(self):
        """Encerra a conexão atual."""
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()
    
    def __send_data(self, data):
        """Constrói um record a partir de dados e envia ele."""
        record = build_record(data)
        self.__socket.sendall(record)
    
    def __receive_data(self):
        """Recebe um record, desempacota ele e retorna os dados."""
        record = self.__socket.recv(RECORD_SIZE)
        return dissect_record(record)

    def get_server_cert(self):
        """Solicita o certificado ao servidor e retorna uma instância de Certificate."""
        self.__send_data(b'Client Hello')
        cert_data = self.__receive_data()
        return x509.load_pem_x509_certificate(cert_data)

    def rcv_client_hello(self):
        """Recebe a mensagem "client hello" e retorna os dados da mensagem."""
        # TODO Rewrite this method
        record = self.__socket.recv(RECORD_SIZE)
        if not record:
            return None
        return dissect_record(record)

    def check_certificate(self, cert):
        """Valida o certificado passado no argumento."""
        common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if common_name != CERT_COMMON_NAME:
            self.close_connection()
            return False

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
            self.__send_data(pem)
    
    def rcv_client_public_key(self):
        """Recebe a chave pública do cliente e retorna uma instância de RSAPublicKey."""
        key_data = self.__receive_data()
        return serialization.load_pem_public_key(key_data)