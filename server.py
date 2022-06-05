import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Server", b"process"]

def accept_wrapper(sock, host, port):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(
            host=host,
            port=port,
            addr=addr,
            recv_total=0,
            sent_total=0,
            messages=list(messages),
            inb=b"",
            outb=b"",
            before_hook=None,
            after_hook_before_socket_close=None,
            after_hook_after_socket_close=None,
        )
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    
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
        dt = [b"Message 1 from server."]
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
        
        if not recv_data and not data.messages:
            print("closing connection", data.addr)
            key.data.after_hook_before_socket_close = after_hook_before_socket_close(sock, data, mask)
            sel.unregister(sock)
            sock.close()
            key.data.after_hook_after_socket_close = after_hook_after_socket_close(sock, data, mask)
        
        if (recv_data.decode() == "exit" or "exit" in recv_data.decode()):
            ex = True
    
    if mask & selectors.EVENT_WRITE:
        if not data.messages and ex:
            print("closing connection", data.addr)
            key.data.after_hook_before_socket_close = after_hook_before_socket_close(sock, data, mask)
            sel.unregister(sock)
            sock.close()
            key.data.after_hook_after_socket_close = after_hook_after_socket_close(sock, data, mask)
        
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        
        if data.outb:
            print("echoing", data.outb, "to", data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj, host, port)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
except Exception as e:
    print("uncaught error, exiting", e)
finally:
    sel.close()

