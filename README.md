# Table of Contents

* [sevp](#sevp)
  * [connect\_to\_server](#sevp.connect_to_server)
  * [check\_certificate](#sevp.check_certificate)
  * [close\_connection](#sevp.close_connection)
  * [handle\_client](#sevp.handle_client)

<a name="sevp"></a>
# sevp

Este módulo fornece suporte ao protocolo de segurança SEVP para sistemas eletrônicos de votação.

<a name="sevp.connect_to_server"></a>
#### connect\_to\_server

```python
connect_to_server()
```

Iniciar uma conexão TCP com o servidor.

<a name="sevp.check_certificate"></a>
#### check\_certificate

```python
check_certificate()
```

Validar o certificado recebido do servidor.

<a name="sevp.close_connection"></a>
#### close\_connection

```python
close_connection(conn)
```

Encerrar conexão.

<a name="sevp.handle_client"></a>
#### handle\_client

```python
handle_client(conn, addr)
```

Tratar de uma conexão (client) em particular.

