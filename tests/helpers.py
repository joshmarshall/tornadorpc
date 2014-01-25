import threading
import time
from tornado.httpclient import AsyncHTTPClient
from tornadorpc import start_server, private, async


class Tree(object):

    def power(self, base, power, modulo=None):
        result = pow(base, power, modulo)
        return result

    def _private(self):
        # Should not be callable
        return False


class TestHandler(object):

    tree = Tree()

    def add(self, x, y):
        return x+y

    @async
    def async(self, url):
        async_client = AsyncHTTPClient()
        async_client.fetch(url, self._handle_response)

    def _handle_response(self, response):
        self.result(response.code)

    @private
    def private(self):
        # Should not be callable
        return False

    def _private(self):
        # Should not be callable
        return False

    def internal_error(self):
        raise Exception("Yar matey!")


class TestServer(object):

    threads = {}

    @classmethod
    def start(cls, handler, port):
        if not cls.threads.get(port):
            cls.threads[port] = threading.Thread(
                target=start_server,
                args=[handler],
                kwargs={'port': port}
            )
            cls.threads[port].daemon = True
            cls.threads[port].start()
            # Giving it time to start up
            time.sleep(1)


class RPCTests(object):

    server = None
    handler = None
    port = 8002

    def setUp(self):
        self.server = TestServer.start(self.handler, self.port)

    def get_url(self):
        return 'http://localhost:%d' % self.port

    def get_client(self):
        raise NotImplementedError("Must return an XML / JSON RPC client.")

    def test_tree(self):
        client = self.get_client()
        result = client.tree.power(2, 6)
        self.assertEqual(result, 64)

    def test_add(self):
        client = self.get_client()
        result = client.add(5, 6)
        self.assertEqual(result, 11)

    def test_async(self):
        url = 'http://www.google.com'
        client = self.get_client()
        result = client.async(url)
        self.assertEqual(result, 200)
