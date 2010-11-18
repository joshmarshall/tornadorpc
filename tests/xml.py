import unittest
import xmlrpclib
import urllib2
import time
import threading
from tornadorpc.xml import XMLRPCHandler
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

class TestXMLHandler(XMLRPCHandler, TestHandler):

    def return_fault(self, code, msg):
        return xmlrpclib.Fault(code, msg)

class TestServer(object):

    threads = {}

    @classmethod
    def start(cls, handler, port):
        if not cls.threads.get(port):
            cls.threads[port] = threading.Thread(
                target=start_server, 
                args=[handler,], 
                kwargs={'port':port}
            )
            cls.threads[port].daemon = True
            cls.threads[port].start()
            # Giving it time to start up
            time.sleep(1)
        
class RPCTests(object):
    
    server = None
    handler = TestXMLHandler
    port = 8002
    
    def setUp(self):
        server = TestServer.start(self.handler, self.port)

    def get_url(self):
        return 'http://localhost:%d' % self.port

    def get_client(self):
        client = xmlrpclib.ServerProxy(self.get_url())
        return client
        
    def test_tree(self):
        client = self.get_client()
        result = client.tree.power(2, 6)
        self.assertTrue(result == 64)
    
    def test_add(self):
        client = self.get_client()
        result = client.add(5, 6)
        self.assertTrue(result == 11)
    
    def test_async(self):
        url = 'http://www.google.com'
        client = self.get_client()
        result = client.async(url)
        self.assertTrue(result == 200)
        
class XMLRPCTests(RPCTests, unittest.TestCase):
        
    def test_private(self):
        client = self.get_client()
        try:
            client.private()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpclib.Fault, f:
            self.assertEqual(-32601, f.faultCode)

    def test_private_by_underscore(self):
        client = self.get_client()
        try:
            client._private()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpclib.Fault, f:
            self.assertEqual(-32601, f.faultCode)

    def test_invalid_params(self):
        client = self.get_client()
        try:
            client.return_fault('a', 'b', 'c')
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpclib.Fault, f:
            self.assertEqual(-32602, f.faultCode)

    def test_internal_error(self):
        client = self.get_client()
        try:
            client.internal_error()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpclib.Fault, f:
            self.assertEqual(-32603, f.faultCode)

    def test_parse_error(self):
        try:
            print self.get_url()
            urllib2.urlopen(self.get_url(), '<garbage/>')
        except xmlrpclib.Fault, f:
            self.assertEqual(-32700, f.faultCode)

    def test_handler_return_fault(self):
        client = self.get_client()
        fault_code = 100
        fault_string = 'Yar matey!'
        try:
            client.return_fault(fault_code, fault_string)
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpclib.Fault, f:
            self.assertEqual(fault_code, f.faultCode)
            self.assertEqual(fault_string, f.faultString)
