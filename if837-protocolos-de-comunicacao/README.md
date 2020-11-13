# Table of Contents

* [sevp](#sevp)
  * [init\_server](#sevp.init_server)
  * [connect\_to\_server](#sevp.connect_to_server)
  * [build\_record](#sevp.build_record)
  * [dissect\_record](#sevp.dissect_record)
  * [SEVPSocket](#sevp.SEVPSocket)
    * [\_\_init\_\_](#sevp.SEVPSocket.__init__)
    * [accept\_incoming\_conn](#sevp.SEVPSocket.accept_incoming_conn)
    * [send\_server\_cert](#sevp.SEVPSocket.send_server_cert)
    * [close\_connection](#sevp.SEVPSocket.close_connection)
    * [get\_server\_cert](#sevp.SEVPSocket.get_server_cert)
    * [rcv\_client\_hello](#sevp.SEVPSocket.rcv_client_hello)
    * [check\_certificate](#sevp.SEVPSocket.check_certificate)
    * [send\_client\_public\_key](#sevp.SEVPSocket.send_client_public_key)
    * [rcv\_client\_public\_key](#sevp.SEVPSocket.rcv_client_public_key)

<a name="sevp"></a>
# sevp

Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.

<a name="sevp.init_server"></a>
#### init\_server

```python
init_server()
```

Inicializa o servidor e retorna uma instância de SEVPSocket.

<a name="sevp.connect_to_server"></a>
#### connect\_to\_server

```python
connect_to_server()
```

Faz uma tentativa de conexão TCP com o servidor e retorna um instância de SEVPSocket.

<a name="sevp.build_record"></a>
#### build\_record

```python
build_record(data)
```

Empacota dados num record SEVP para ser enviado pelo socket e retorna o record.

<a name="sevp.dissect_record"></a>
#### dissect\_record

```python
dissect_record(record)
```

Desempacota os campos de um record e retorna o dado em bytes.

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

Inicializa o objeto com o socket passado no contrutor da classe.

<a name="sevp.SEVPSocket.accept_incoming_conn"></a>
#### accept\_incoming\_conn

```python
 | accept_incoming_conn()
```

Habilita o servidor para aceitar uma conexão de chegada.

<a name="sevp.SEVPSocket.send_server_cert"></a>
#### send\_server\_cert

```python
 | send_server_cert()
```

Efetua o envio do certificado do servidor.

<a name="sevp.SEVPSocket.close_connection"></a>
#### close\_connection

```python
 | close_connection()
```

Encerra a conexão atual.

<a name="sevp.SEVPSocket.get_server_cert"></a>
#### get\_server\_cert

```python
 | get_server_cert()
```

Solicita o certificado ao servidor e retorna uma instância de Certificate.

<a name="sevp.SEVPSocket.rcv_client_hello"></a>
#### rcv\_client\_hello

```python
 | rcv_client_hello()
```

Recebe a mensagem "client hello" e retorna os dados da mensagem.

<a name="sevp.SEVPSocket.check_certificate"></a>
#### check\_certificate

```python
 | check_certificate(cert)
```

Valida o certificado passado no argumento.

<a name="sevp.SEVPSocket.send_client_public_key"></a>
#### send\_client\_public\_key

```python
 | send_client_public_key()
```

Envia a chave pública do cliente.

<a name="sevp.SEVPSocket.rcv_client_public_key"></a>
#### rcv\_client\_public\_key

```python
 | rcv_client_public_key()
```

Recebe a chave pública do cliente e retorna uma instância de RSAPublicKey.

