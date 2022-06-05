import socket
# Socket's Listeners
from taskcontrol.lib import SocketsBase

Socket = SocketsBase()

# def client_handler(messages, socket_client, instance_object):
#     c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     c.connect("127.0.0.1", 9001)
#     c.send("Hello From Client".decode())
#     c.recv(1024).decode()

#     # server_addr = ((socket_client.get("host"), socket_client.get("port")))
#     # socket_client.get("server").connect(server_addr)
#     # for idx, m in enumerate(messages):
#     #     socket_client.get("server").sendall(
#     #         "Testing the client message\n".encode())
#     #     socket_client.get("server").sendall(messages[idx])
#     # while True:
#     #     data = socket_client.get("server").recv(1024).decode()
#     #     if data:
#     #         print("Data \n", data)
#     #     else:
#     #         socket_client.get("server").send("close".encode())
#     #     break
#     # socket_client.get("server").close()
#     # print("CLIENT ", socket_client.get("host"), socket_client.get("port"))

def client_handler(sobject, messages, instance_object):
    print("test")
    sobject.get("server").connect((sobject.get("host"), sobject.get("port")))
    sobject.get("server").send(b'Hello, world')
    data = sobject.get("server").recv(1024)

config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": client_handler, "close_server": True}

cl = Socket.socket_connect(config, [b"Testing message from client"])
