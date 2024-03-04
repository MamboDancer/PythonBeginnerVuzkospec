import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:1515")
print(c.rpc_hello("pedik"))
