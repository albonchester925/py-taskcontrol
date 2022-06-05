import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Client", b"process"]


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            host=host,
            port=port,
            addr=port,
            recv_total=0,
            sent_total=0,
            messages=list(messages),
            inb=b"",
            outb=b"",
            before_hook=None,
            after_hook_before_close=None,
            after_hook_after_close=None,
        )
        sel.register(sock, events, data=data)


def service_connection(key, mask):

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
        dt = [b"Hello 1 from Client."]
        dt += [b"exit"]
        return dt
    
    sock = key.fileobj
    data = key.data
    ex = False

    if not data.inb and not data.outb:
        key.data.before_hook = before_hook(sock, data, mask)
    
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        print("received", repr(recv_data), "from connection", data.connid)
        
        if recv_data:
            data.recv_total += len(recv_data)
            data.inb += recv_data
            if (recv_data.decode() == "process" or "process" in recv_data.decode()):
                data.messages += list(process_data(key, mask, data.inb))
        
        if not recv_data and not data.messages:
            print("closing connection", data.connid)
            key.data.after_hook_before_close = after_hook_before_close(sock, data, mask)
            sel.unregister(sock)
            sock.close()
            key.data.after_hook_after_close = after_hook_after_close(sock, data, mask)
        
        if (recv_data.decode() == "exit" or "exit" in recv_data.decode()):
            ex = True
    
    if mask & selectors.EVENT_WRITE:
        if not data.messages and ex:
            print("closing connection", data.connid)
            key.data.after_hook_before_close = after_hook_before_close(sock, data, mask)
            sel.unregister(sock)
            sock.close()
            key.data.after_hook_after_close = after_hook_after_close(sock, data, mask)
        
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        
        if data.outb and data.inb:
            print("sending", data.outb, "to connection", data.connid)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]    

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        else:
            break
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
except Exception as e:
    print("uncaught error, exiting", e)
finally:
    sel.close()
    sys.exit(1)
