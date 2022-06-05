import socket
import selectors
# Socket's Listeners
from taskcontrol.lib import SocketsBase

Socket = SocketsBase()

def client_blocking_handler(messages, socket_object, instance_object):
    """
    Applies for numbers: 1
    """
    pass


def client_nonblocking_handler(key, mask, sel, socket_object, messages, instance_object):
    """
    Applies for numbers > 1
    """

    def before_hook(sock, data, mask):
        print("before_hook")
        return []

    def after_hook_before_close(sock, data, mask):
        print("after_hook_before_close")
        return []

    def after_hook_after_close(sock, data, mask):
        print("after_hook_after_close")
        return []

    def process_data(key, mask, d=b"exit"):
        print("Server Data Received", d)
        dt = [b"Hello from Client."]
        dt += [b"exit"]
        return dt

    result = None
    sock = key.fileobj
    data = key.data
    ex = False

    # if not data.inb and not data.outb:
    #     key.data.before_hook = before_hook(sock, data, mask)

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
            data.inb += recv_data
            if (recv_data.decode() == "process" or "process" in recv_data.decode()):
                data.messages += list(process_data(key, mask, data.inb))

        if not recv_data and not data.messages and socket_object.get("close_server", True):
            print("closing connection", data.connid)
            # key.data.after_hook_before_close = after_hook_before_close(
            #     sock, data, mask)
            sel.unregister(sock)
            sock.close()
            # key.data.after_hook_after_close = after_hook_after_close(
            #     sock, data, mask)

        if (recv_data.decode() == "exit" or "exit" in recv_data.decode()):
            ex = True

    if mask & selectors.EVENT_WRITE:
        if not data.messages and ex and socket_object.get("close_server", True):
            print("closing connection", data.connid)
            # key.data.after_hook_before_close = after_hook_before_close(
            #     sock, data, mask)
            sel.unregister(sock)
            sock.close()
            # key.data.after_hook_after_close = after_hook_after_close(
            #     sock, data, mask)

        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)

        if data.outb and data.inb:
            print("sending", data.outb, "to connection", data.connid)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
    return socket_object, data, result


# # NON-BLOCKING HANDLER - SINGLE CONNECTION
# config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
#           "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": client_blocking_handler,
#           "blocking": False, "close_server": True}

# Socket.socket_connect(
#     config, [b"Message 1 from client.", b"Message 2 from client.", b"process"])


# NON-BLOCKING HANDLER - SINGLE CONNECTION
config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": client_nonblocking_handler,
          "blocking": False, "close_server": True}

Socket.socket_connect(
    config, [b"Message 1 from client.", b"Message 2 from client.", b"process"])

# NON-BLOCKING HANDLER - MULTIPLE CONNECTION
# config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
#           "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": client_nonblocking_handler,
#           "blocking": False, "close_server": False}

# Socket.socket_connect(
#     config, [b"Message 1 from client.", b"Message 2 from client.", b"process"])
