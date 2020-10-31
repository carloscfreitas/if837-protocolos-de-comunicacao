# Secure Eletronic Voting Protocol

"""Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.
"""

import cryptography
import socket

SERVER_HOST = 'localhost'
SERVER_PORT = 50008

def connect_to_server(): 
    """Iniciar uma conexão TCP com o servidor."""
    pass

def check_certificate():
    """Validar o certificado recebido do servidor."""
    pass

def close_connection(conn):
    """Encerrar conexão."""
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def handle_client(conn, addr):
    """Tratar de uma conexão (client) em particular."""
    while True:
        data = conn.recv(1024)
        if not data: 
            print('Bye', addr) 
            break
        # reverse the given string
        data = data[::-1]
        conn.sendall(data)
    close_connection(conn)
