import socket
import selectors
# Socket's Listeners
from taskcontrol.lib import SocketsBase


Socket = SocketsBase()


def server_blocking_handler(conn, addr, socket_server):
    print("SERVER", conn, addr)
    while True:
        data = conn.recv(1024).decode()
        if data:
            print("Data \n", data)
            if data == "close":
                conn.close()
            else:
                conn.send("close".encode())
        break
    conn.close()
    print("SERVER ", socket_server.get("host"), socket_server.get("port"))
    # print(socket_server.get("server").close())


def server_nonblocking_handler(key, mask, sel, socket_object, instance_object):
    try:
        def before_hook(sock, data, mask):
            print("before_hook")
            return []

        def after_hook_before_socket_close(sock, data, mask):
            print("after_hook_before_socket_close")
            return []

        def after_hook_after_socket_close(sock, data, mask):
            print("after_hook_after_socket_close")
            return []

        def process_data(key, mask, d=b"exit"):
            print("Client Data Received", d)
            dt = [b"Hello from server."]
            dt += [b"exit"]
            return dt

        sock = key.fileobj
        data = key.data
        ex = False

        if not data.inb and not data.outb:
            key.data.before_hook = before_hook(sock, data, mask)

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            print("received", repr(recv_data), "from connection", data.addr)

            if recv_data:
                data.inb += recv_data
                if (recv_data.decode() == "process" or "process" in recv_data.decode()):
                    data.messages += list(process_data(key, mask, data.inb))

            if not recv_data and not data.messages and socket_object.get("close_server", True):
                print("closing connection", data.addr)
                # key.data.after_hook_before_socket_close = after_hook_before_socket_close(
                #     sock, data, mask)
                sel.unregister(sock)
                sock.close()
                # key.data.after_hook_after_socket_close = after_hook_after_socket_close(
                #     sock, data, mask)

            if (recv_data.decode() == "exit" or "exit" in recv_data.decode()):
                ex = True

        if mask & selectors.EVENT_WRITE:
            if not data.messages and ex and socket_object.get("close_server", True):
                print("closing connection", data.addr)
                # key.data.after_hook_before_socket_close = after_hook_before_socket_close(
                #     sock, data, mask)
                sel.unregister(sock)
                sock.close()
                # key.data.after_hook_after_socket_close = after_hook_after_socket_close(
                #     sock, data, mask)

            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)

            if data.outb:
                print("echoing", data.outb, "to", data.addr)
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
        return True
    except Exception as e:
        print("Error in service connection: service_connection ", e)
        return False

# NON-BLOCKING HANDLER - SINGLE CONNECTION
# config = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
#           "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": True, "close_server": True}

# s = Socket.socket_create(config)

# NON-BLOCKING HANDLER - SINGLE OR MULTIPLE CONNECTIONS
config = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False, "close_server": True}

s = Socket.socket_create(config)

if s:
    print("Server started")
    sr = Socket.socket_listen(config.get("name"))
