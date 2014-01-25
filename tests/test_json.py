from tests.helpers import TestHandler, RPCTests
from tornadorpc.json import JSONRPCHandler
import jsonrpclib
import unittest


class JSONTestHandler(TestHandler, JSONRPCHandler):

    def order(self, a=1, b=2, c=3):
        return {'a': a, 'b': b, 'c': c}


class JSONRPCTests(RPCTests, unittest.TestCase):

    port = 8003
    handler = JSONTestHandler

    def get_client(self):
        client = jsonrpclib.Server('http://localhost:%d' % self.port)
        return client

    def test_private(self):
        client = self.get_client()
        self.assertRaises(jsonrpclib.ProtocolError, client.private)

    def test_order(self):
        client = self.get_client()
        self.assertEqual(
            client.order(), {'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(
            client.order(a=10), {'a': 10, 'b': 2, 'c': 3})
        self.assertEqual(
            client.order(c=10), {'a': 1, 'b': 2, 'c': 10})
        self.assertEqual(
            client.order(a=10, b=11, c=12), {'a': 10, 'b': 11, 'c': 12})
