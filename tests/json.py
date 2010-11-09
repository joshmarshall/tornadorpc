from tests.xml import TestHandler, RPCTests
from tornadorpc.json import JSONRPCHandler
import jsonrpclib
import unittest

class TestJSONHandler(TestHandler, JSONRPCHandler):
    pass
            
class JSONRPCTests(RPCTests, unittest.TestCase):
    port = 8003
    handler = TestJSONHandler
    
    def get_client(self):
        client = jsonrpclib.Server('http://localhost:%d' % self.port)
        return client
        
    def test_private(self):
        client = self.get_client()
        self.assertRaises(jsonrpclib.ProtocolError, client.private)

