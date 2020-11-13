# Table of Contents

* [sevp](#sevp)
  * [start\_server](#sevp.start_server)
  * [connect\_to\_server](#sevp.connect_to_server)
  * [build\_record](#sevp.build_record)
  * [dissect\_record](#sevp.dissect_record)
  * [load\_private\_key](#sevp.load_private_key)
  * [load\_certificate](#sevp.load_certificate)
  * [SEVPSocket](#sevp.SEVPSocket)
    * [\_\_init\_\_](#sevp.SEVPSocket.__init__)
    * [send\_message](#sevp.SEVPSocket.send_message)
    * [receive\_message](#sevp.SEVPSocket.receive_message)
    * [close\_connection](#sevp.SEVPSocket.close_connection)
  * [ClientSocket](#sevp.ClientSocket)
    * [\_\_init\_\_](#sevp.ClientSocket.__init__)
    * [do\_handshake](#sevp.ClientSocket.do_handshake)
    * [get\_server\_cert](#sevp.ClientSocket.get_server_cert)
    * [check\_certificate](#sevp.ClientSocket.check_certificate)
    * [send\_client\_public\_key](#sevp.ClientSocket.send_client_public_key)
    * [rcv\_secret\_key](#sevp.ClientSocket.rcv_secret_key)
    * [send\_encrypted\_msn](#sevp.ClientSocket.send_encrypted_msn)
    * [rcv\_encrypted\_msn](#sevp.ClientSocket.rcv_encrypted_msn)
  * [ServerSocket](#sevp.ServerSocket)
    * [\_\_init\_\_](#sevp.ServerSocket.__init__)
    * [accept\_incoming\_conn](#sevp.ServerSocket.accept_incoming_conn)
    * [do\_handshake](#sevp.ServerSocket.do_handshake)
    * [send\_server\_cert](#sevp.ServerSocket.send_server_cert)
    * [rcv\_client\_hello](#sevp.ServerSocket.rcv_client_hello)
    * [rcv\_client\_public\_key](#sevp.ServerSocket.rcv_client_public_key)
    * [send\_secret\_key](#sevp.ServerSocket.send_secret_key)
    * [send\_encrypted\_msn](#sevp.ServerSocket.send_encrypted_msn)
    * [rcv\_encrypted\_msn](#sevp.ServerSocket.rcv_encrypted_msn)
  * [Message](#sevp.Message)
    * [\_\_init\_\_](#sevp.Message.__init__)
    * [mac](#sevp.Message.mac)
    * [encrypt](#sevp.Message.encrypt)
    * [decrypt](#sevp.Message.decrypt)
    * [verify](#sevp.Message.verify)
    * [separate\_data\_from\_mac](#sevp.Message.separate_data_from_mac)

<a name="sevp"></a>
# sevp

Este módulo fornece suporte em Python ao protocolo de segurança SEVP
para sistemas eletrônicos de votação.

<a name="sevp.start_server"></a>
#### start\_server

```python
start_server()
```

Inicialize o servidor e retorne um objeto ServerSocket.

<a name="sevp.connect_to_server"></a>
#### connect\_to\_server

```python
connect_to_server()
```

Faça uma conexão TCP com o servidor e retorne um objeto ClientSocket.

<a name="sevp.build_record"></a>
#### build\_record

```python
build_record(message)
```

Empacote um objeto Message num record SEVP e retorne o record.

<a name="sevp.dissect_record"></a>
#### dissect\_record

```python
dissect_record(record)
```

Desempacote os campos de um record e retorne uma instância de Message.

<a name="sevp.load_private_key"></a>
#### load\_private\_key

```python
load_private_key(path, password)
```

Carregue em memória uma chave privada e retorne um objeto RSAPrivateKey.

<a name="sevp.load_certificate"></a>
#### load\_certificate

```python
load_certificate(path)
```

Carregue um certificado em memória e retorne um objeto Certificate.

<a name="sevp.SEVPSocket"></a>
## SEVPSocket Objects

```python
class SEVPSocket()
```

<a name="sevp.SEVPSocket.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(socket)
```

Construa um objeto SEVPSocket.

<a name="sevp.SEVPSocket.send_message"></a>
#### send\_message

```python
 | send_message(message)
```

Serialize um objeto Message e o envie pelo socket.

<a name="sevp.SEVPSocket.receive_message"></a>
#### receive\_message

```python
 | receive_message()
```

Receba um record pelo socket, desempacote o record e retorne um objeto Message.

<a name="sevp.SEVPSocket.close_connection"></a>
#### close\_connection

```python
 | close_connection()
```

Feche imediatamente a conexão atual.

<a name="sevp.ClientSocket"></a>
## ClientSocket Objects

```python
class ClientSocket(SEVPSocket)
```

<a name="sevp.ClientSocket.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(socket)
```

Construa um objeto ClientSocket.

<a name="sevp.ClientSocket.do_handshake"></a>
#### do\_handshake

```python
 | do_handshake()
```

Execute o handshake, estabelecendo uma conexão segura.

<a name="sevp.ClientSocket.get_server_cert"></a>
#### get\_server\_cert

```python
 | get_server_cert()
```

Solicite o certificado ao servidor e o retorne como um objeto Certificate.

<a name="sevp.ClientSocket.check_certificate"></a>
#### check\_certificate

```python
 | check_certificate(cert)
```

Valide a assinatura e o CN do certificado.

<a name="sevp.ClientSocket.send_client_public_key"></a>
#### send\_client\_public\_key

```python
 | send_client_public_key()
```

Envie a chave pública.

<a name="sevp.ClientSocket.rcv_secret_key"></a>
#### rcv\_secret\_key

```python
 | rcv_secret_key()
```

Receba a chave secreta para geração do MAC.

<a name="sevp.ClientSocket.send_encrypted_msn"></a>
#### send\_encrypted\_msn

```python
 | send_encrypted_msn(code, data)
```

Envie dados encriptados com a chave pública do servidor.

<a name="sevp.ClientSocket.rcv_encrypted_msn"></a>
#### rcv\_encrypted\_msn

```python
 | rcv_encrypted_msn()
```

Receba dados encriptados, os desencripte e verifique sua integridade e autenticidade.

<a name="sevp.ServerSocket"></a>
## ServerSocket Objects

```python
class ServerSocket(SEVPSocket)
```

<a name="sevp.ServerSocket.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(socket)
```

Construa um objeto ServerSocket.

<a name="sevp.ServerSocket.accept_incoming_conn"></a>
#### accept\_incoming\_conn

```python
 | accept_incoming_conn()
```

Habilite o servidor para aceitar uma conexão de chegada e retorne
uma tupla (ServerSocket, endereço).

<a name="sevp.ServerSocket.do_handshake"></a>
#### do\_handshake

```python
 | do_handshake()
```

Execute o handshake, estabelecendo uma conexão segura.

<a name="sevp.ServerSocket.send_server_cert"></a>
#### send\_server\_cert

```python
 | send_server_cert()
```

Efetue o envio do certificado.

<a name="sevp.ServerSocket.rcv_client_hello"></a>
#### rcv\_client\_hello

```python
 | rcv_client_hello()
```

Receba a mensagem "client hello" e retorne um objeto Message.

<a name="sevp.ServerSocket.rcv_client_public_key"></a>
#### rcv\_client\_public\_key

```python
 | rcv_client_public_key()
```

Recebe a chave pública do cliente e retorna uma instância de RSAPublicKey.

<a name="sevp.ServerSocket.send_secret_key"></a>
#### send\_secret\_key

```python
 | send_secret_key()
```

Gere uma chave secreta para geração de MAC e a envie.

<a name="sevp.ServerSocket.send_encrypted_msn"></a>
#### send\_encrypted\_msn

```python
 | send_encrypted_msn(code, data)
```

Envie dados encriptados com a chave pública do cliente.

<a name="sevp.ServerSocket.rcv_encrypted_msn"></a>
#### rcv\_encrypted\_msn

```python
 | rcv_encrypted_msn()
```

Receba dados encriptados, os desencripte e verifique sua integridade e autenticidade.

<a name="sevp.Message"></a>
## Message Objects

```python
class Message()
```

<a name="sevp.Message.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data, code=1, mac_key=None)
```

Construa um objeto Message.

<a name="sevp.Message.mac"></a>
#### mac

```python
 | mac(mac_key)
```

Gere o MAC de um dado a partir de uma chave e retorne o MAC.

<a name="sevp.Message.encrypt"></a>
#### encrypt

```python
 | encrypt(public_key)
```

Encripte os dados, possivelmente concatenados com o MAC, utilizando uma chave.

<a name="sevp.Message.decrypt"></a>
#### decrypt

```python
 | decrypt(private_key)
```

Desencripte os dados utilizando uma chave.

<a name="sevp.Message.verify"></a>
#### verify

```python
 | verify(mac_key)
```

Verifique se a mensagem corresponde ao MAC contido nos dados.

<a name="sevp.Message.separate_data_from_mac"></a>
#### separate\_data\_from\_mac

```python
 | separate_data_from_mac()
```

Separe os bytes referentes aos dados (aplicação) dos referentes ao MAC.

