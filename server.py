import zerorpc


class HelloRPC(object):
    number = 10
    def hello(self, name):
        return "Hello, %s" % name

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number


s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()