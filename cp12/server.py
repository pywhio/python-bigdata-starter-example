import socketserver , io
from decompress import decompress
from serializer import serialize, deserialize

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(102400000)
        print("%s send zipbytes %d" % (self.client_address[0], len(self.data)))
        result = decompress(io.BytesIO(self.data))
        # just send back the same data, but upper-cased
        self.request.sendall(serialize(result))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
