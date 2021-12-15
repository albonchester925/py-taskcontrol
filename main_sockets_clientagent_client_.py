import socket
import selectors
# Socket's Listeners
from taskcontrol.lib import SocketsBase, UtilsBase, ConcurencyBase


def server_blocking_handler(conn, addr, socket_object):
    pass



def server_nonblocking_handler(key, mask, socket_object, instance_object):
    
    def server_processing(action, event):
        print(action, event)
        return {"result": "Test"}
    
    sock = key.fileobj
    data = key.data
    sel = socket_object.get("selectors")
    if mask & selectors.EVENT_READ:
        # Should be ready to read
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
            if data:
                json_dict = UtilsBase.json_to_dict(data)
                action = json_dict.get("action")
                event = json_dict.get("event")
                result = server_processing(action, event)
                if result != None:
                    if result.get("message", None) != None:
                        result_message = conn.sendall(result.get("message"))
                    if result_message != None:
                        pass
        else:
            print("Closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(
                data.outb), "to", data.addr)
            # Should be ready to write
            sent = sock.sendall(data.outb)
            data.outb = data.outb[sent:]
        # sock.close()
        # return False
    sock.close()


# def serverfunction():
Socket = SocketsBase()
config = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM, "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}
s = Socket.socket_create(config)
print("s", s)
if s:
    print("Server started")
    sr = Socket.socket_listen(config.get("name"))

# proc = ConcurencyBase.thread(target=serverfunction, daemon=True)
# print(proc)

# INC000013517446
