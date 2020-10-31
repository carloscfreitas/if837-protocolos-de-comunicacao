# Table of Contents

* [sevp](#sevp)
  * [connect\_to\_server](#sevp.connect_to_server)
  * [check\_certificate](#sevp.check_certificate)
  * [close\_connection](#sevp.close_connection)
  * [handle\_client](#sevp.handle_client)
  * [build\_record](#sevp.build_record)
  * [dissect\_record](#sevp.dissect_record)

<a name="sevp"></a>
# sevp

Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.

<a name="sevp.connect_to_server"></a>
#### connect\_to\_server

```python
connect_to_server()
```

Inicie uma conexão TCP com o servidor.

<a name="sevp.check_certificate"></a>
#### check\_certificate

```python
check_certificate()
```

Valide o certificado recebido do servidor.

<a name="sevp.close_connection"></a>
#### close\_connection

```python
close_connection(conn)
```

Encerre a conexão.

<a name="sevp.handle_client"></a>
#### handle\_client

```python
handle_client(conn, addr)
```

Trate de uma conexão (client) em particular.

<a name="sevp.build_record"></a>
#### build\_record

```python
build_record(data)
```

Crie um record para ser enviado através do socket.

<a name="sevp.dissect_record"></a>
#### dissect\_record

```python
dissect_record(record)
```

Desempacote os campos de um record.

