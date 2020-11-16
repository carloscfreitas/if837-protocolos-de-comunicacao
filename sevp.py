# Secure Electronic Voting Protocol (SEVP)

"""Este módulo fornece suporte em Python ao protocolo de segurança SEVP
para sistemas eletrônicos de votação.
"""

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, hmac, serialization
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
#       CODE: 1-byte integer, "B"
#       DLC (Data Length Code): 2-byte integer, "H"
#       DATA: 2048-byte string, "2048s"
RECORD_FMT = "!BH2048s"
RECORD_SIZE = struct.calcsize(RECORD_FMT)

CERT_COMMON_NAME = 'electronicvoting.com'

CLIENT_PVT_KEY_PATH = "certs/client_key.pem"
CLIENT_PVT_KEY_PWD = b"client"
SERVER_PVT_KEY_PATH = "certs/server_key.pem"
SERVER_PVT_KEY_PWD = b"server"
SERVER_CERT_PATH = "certs/certificate.pem"

MESSAGE_CODE_PROMPT = 1
MESSAGE_CODE_END_SESSION = 255

def start_server():
    """Inicialize o servidor e retorne um objeto ServerSocket."""
    sock = socket.create_server((SERVER_HOST, SERVER_PORT))
    return ServerSocket(sock)

def connect_to_server():
    """Faça uma conexão TCP com o servidor e retorne um objeto ClientSocket."""
    sock = socket.create_connection((SERVER_HOST, SERVER_PORT))
    return ClientSocket(sock)

def build_record(message):
    """Empacote um objeto Message num record SEVP e retorne o record."""
    record_dlc = len(message.data)
    return struct.pack(RECORD_FMT, message.code, record_dlc, message.data)

def dissect_record(record):
    """Desempacote os campos de um record e retorne uma instância de Message."""
    code, record_dlc, data = struct.unpack(RECORD_FMT, record)
    return Message(data=data[:record_dlc], code=code)

def load_private_key(path, password):
    """Carregue em memória uma chave privada e retorne um objeto RSAPrivateKey."""
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=password)

def load_certificate(path):
    """Carregue um certificado em memória e retorne um objeto Certificate."""
    with open(path, "rb") as cert_file:
        return x509.load_pem_x509_certificate(cert_file.read())

class SEVPSocket():
    def __init__(self, socket):
        """Construa um objeto SEVPSocket."""
        self.socket = socket
    
    def send_message(self, message):
        """Serialize um objeto Message e o envie pelo socket."""
        record = build_record(message)
        self.socket.sendall(record)

    def receive_message(self):
        """Receba um record pelo socket, desempacote o record e retorne um objeto Message."""
        record = self.socket.recv(RECORD_SIZE)
        return dissect_record(record)

    def close_connection(self):
        """Feche imediatamente a conexão atual."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

class ClientSocket(SEVPSocket):
    def __init__(self, socket):
        """Construa um objeto ClientSocket."""
        super().__init__(socket)
        self.server_cert = None
        self.server_pub_key = None
        self.client_prv_key = load_private_key(CLIENT_PVT_KEY_PATH, CLIENT_PVT_KEY_PWD)
        self.client_pub_key = self.client_prv_key.public_key()
        self.secret_key = None

    def do_handshake(self):
        """Execute o handshake, estabelecendo uma conexão segura."""
        cert = self.get_server_cert()
        self.check_certificate(cert)
        self.send_client_public_key()
        self.rcv_secret_key()

    def get_server_cert(self):
        """Solicite o certificado ao servidor e o retorne como um objeto Certificate."""
        self.send_message(Message(data=b'Client Hello'))
        message = self.receive_message()
        self.server_cert = x509.load_pem_x509_certificate(message.data)
        self.server_pub_key = self.server_cert.public_key()
        return self.server_cert
    
    def check_certificate(self, cert):
        """Valide a assinatura e o CN do certificado."""
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
        """Envie a chave pública."""
        pem = self.client_pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.send_message(Message(data=pem))
    
    def rcv_secret_key(self):
        """Receba a chave secreta para geração do MAC."""
        message = self.rcv_encrypted_msn()
        self.secret_key = message.data
        return self.secret_key
    
    def send_encrypted_msn(self, code, data):
        """Envie dados encriptados com a chave pública do servidor."""
        message = Message(data, code, self.secret_key)
        message.encrypt(self.server_pub_key)
        self.send_message(message)

    def rcv_encrypted_msn(self):
        """Receba dados encriptados, os desencripte e verifique sua integridade e autenticidade."""
        message = self.receive_message()
        message.decrypt(self.client_prv_key)
        message.verify(self.secret_key)
        return message

class ServerSocket(SEVPSocket):
    def __init__(self, socket):
        """Construa um objeto ServerSocket."""
        super().__init__(socket)
        self.server_cert = load_certificate(SERVER_CERT_PATH)
        self.server_pub_key = self.server_cert.public_key()
        self.server_prv_key = load_private_key(SERVER_PVT_KEY_PATH, SERVER_PVT_KEY_PWD)
        self.client_pub_key = None
        self.secret_key = None
    
    def accept_incoming_conn(self):
        """Habilite o servidor para aceitar uma conexão de chegada e retorne
        uma tupla (ServerSocket, endereço)."""
        conn, addr = self.socket.accept()
        return ServerSocket(conn), addr

    def do_handshake(self):
        """Execute o handshake, estabelecendo uma conexão segura."""
        self.rcv_client_hello()
        self.send_server_cert()
        self.rcv_client_public_key()
        self.send_secret_key()

    def send_server_cert(self):
        """Efetue o envio do certificado."""
        cert_data = self.server_cert.public_bytes(serialization.Encoding.PEM)
        self.send_message(Message(data=cert_data))

    def rcv_client_hello(self):
        """Receba a mensagem "client hello" e retorne um objeto Message."""
        return self.receive_message()
    
    def rcv_client_public_key(self):
        """Recebe a chave pública do cliente e retorna uma instância de RSAPublicKey."""
        message = self.receive_message()
        self.client_pub_key = serialization.load_pem_public_key(message.data)
        return self.client_pub_key
    
    def send_secret_key(self):
        """Gere uma chave secreta para geração de MAC e a envie."""
        secret_key = os.urandom(32)
        self.send_encrypted_msn(2, secret_key)
        self.secret_key = secret_key
    
    def send_encrypted_msn(self, code, data):
        """Envie dados encriptados com a chave pública do cliente."""
        message = Message(data, code, self.secret_key)
        message.encrypt(self.client_pub_key)
        self.send_message(message)
    
    def rcv_encrypted_msn(self):
        """Receba dados encriptados, os desencripte e verifique sua integridade e autenticidade."""
        message = self.receive_message()
        message.decrypt(self.server_prv_key)
        message.verify(self.secret_key)
        return message

class Message():
    def __init__(self, data, code=1, mac_key=None):
        """Construa um objeto Message."""
        self.code = code
        self.data = data
        self.MAC = self.mac(mac_key)
    
    def mac(self, mac_key):
        """Gere o MAC de um dado a partir de uma chave e retorne o MAC."""
        mac = None
        if mac_key and self.data:
            h = hmac.HMAC(mac_key, hashes.SHA256())
            h.update(self.data)
            mac = h.finalize()
        return mac

    def encrypt(self, public_key):
        """Encripte os dados, possivelmente concatenados com o MAC, utilizando uma chave."""
        message = self.data
        if self.MAC:
            message = self.data + self.MAC

        self.data = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, private_key):
        """Desencripte os dados utilizando uma chave."""
        self.data = private_key.decrypt(
            self.data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def verify(self, mac_key):
        """Verifique se a mensagem corresponde ao MAC contido nos dados."""
        if mac_key:
            data, mac = self.separate_data_from_mac()
            h = hmac.HMAC(mac_key, hashes.SHA256())
            h.update(data)
            h.verify(mac)
            self.data = data
            self.MAC = mac

    def separate_data_from_mac(self):
        """Separe os bytes referentes aos dados (aplicação) dos referentes ao MAC."""
        # Every byte up to the last 32 bytes
        data = self.data[:-32]
        # Last 32 bytes (digest_size length for SHA256)
        mac = self.data[-32:]
        return data, mac