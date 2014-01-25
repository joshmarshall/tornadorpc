import json
from tests.helpers import TestHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncHTTPTestCase
import tornado.web
from tornadorpc import async
from tornadorpc.xml import XMLRPCHandler
import xmlrpclib


class AsyncHandler(XMLRPCHandler, TestHandler):

    @async
    def async_method(self, url):
        async_client = AsyncHTTPClient()
        async_client.fetch(url, self._handle_response)

    @async
    def bad_async_method(self, url):
        async_client = AsyncHTTPClient()
        async_client.fetch(url, self._handle_response)
        return 5

    def _handle_response(self, response):
        self.result(json.loads(response.body))


class AsyncXMLRPCClient(object):

    def __init__(self, url, ioloop, fetcher):
        self._url = url
        self._ioloop = ioloop
        self._fetcher = fetcher

    def __getattr__(self, attribute):
        return Caller(attribute, self)

    def execute(self, method, params, keyword_params):
        if params and keyword_params:
            raise Exception(
                "Can't have both keyword and positional arguments.")
        arguments = params or keyword_params
        body = xmlrpclib.dumps(arguments, methodname=method)
        response = self._fetcher(self._url, method="POST", body=body)
        result, _ = xmlrpclib.loads(response.body)
        return result[0]


class Caller(object):

    def __init__(self, namespace, client):
        self._namespace = namespace
        self._client = client

    def __getattr__(self, namespace):
        self._namespace += "." + namespace
        return self

    def __call__(self, *args, **kwargs):
        return self._client.execute(self._namespace, args, kwargs)


class AsyncTests(AsyncHTTPTestCase):

    def get_app(self):

        class IndexHandler(tornado.web.RequestHandler):

            def get(self):
                self.finish({"foo": "bar"})

        return tornado.web.Application([
            ("/", IndexHandler),
            ("/RPC2", AsyncHandler)
        ])

    def get_client(self):
        return AsyncXMLRPCClient(
            url="/RPC2", ioloop=self.io_loop, fetcher=self.fetch)

    def test_async_method(self):
        client = self.get_client()
        result = client.async_method(
            "http://localhost:%d/" % (self.get_http_port()))
        self.assertEqual({"foo": "bar"}, result)

    def test_async_returns_non_none_raises_internal_error(self):
        client = self.get_client()
        try:
            client.bad_async_method(
                "http://localhost:%d/" % (self.get_http_port()))
            self.fail("xmlrpclib.Fault should have been raised.")
        except xmlrpclib.Fault, fault:
            self.assertEqual(-32603, fault.faultCode)
