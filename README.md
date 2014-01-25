[![Build Status](https://travis-ci.org/joshmarshall/tornadorpc.png?branch=master)](https://travis-ci.org/joshmarshall/tornadorpc)
TORNADO-RPC
===========
This library is an implementation of both the JSON-RPC and the
XML-RPC specification (server-side) for the Tornado web framework.
It supports the basic features of both, as well as the MultiCall /
Batch support for both specifications. The JSON-RPC handler supports 
both the original 1.0 specification, as well as the new (proposed) 
2.0 spec, which includes batch submission, keyword arguments, etc.

Asynchronous request support has been added for methods which require 
the use of asynchronous libraries (like Tornado's AsyncHTTPClient 
library.)

TornadoRPC is licensed under the Apache License, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0.html).

Mailing List
------------
If you have any questions, issues, or just use the library please feel 
free to send a message to the mailing list at:

    http://groups.google.com/group/tornadorpc

Installation
------------
To install:

    python setup.py build
    sudo python setup.py install

To use this module, you'll need Tornado installed, which you can
get at this address:

http://www.tornadoweb.org/

If you want to use the JSON-RPC handler, you'll also need 
jsonrpclib, which you can grab at:

http://github.com/joshmarshall/jsonrpclib/

The jsonrpclib library requires one of the JSON libraries. It looks 
first for cjson, then for the built-in JSON library (with default 
Python 2.6+ distributions), and finally the simplejson library.

Overview
--------
This library is an implementation of both the JSON-RPC and the XML-RPC 
specification (server-side) for the Tornado web framework. It supports 
the basic features of both, as well as the MultiCall / Batch support for 
both specifications. The JSON-RPC handler supports both the original 1.0 
specification, as well as the new (proposed) 2.0 spec, which includes batch 
submission, keyword arguments, etc. 

There is also a base library that other RPC protocols could use to quickly 
get tied into Tornado.

Requirements
------------
The library obviously requires Tornado, which you can get at 
Tornado's website (http://www.tornadoweb.org). After installing Tornado 
(instructions included with the Tornado distribution) you should be able 
to use the XML-RPC handler without any other libraries.

The JSON-RPC handler requires my jsonrpclib library, which you can get 
at http://github.com/joshmarshall/jsonrpclib . It also requires a JSON 
library, although any distribution of Python past 2.5 should have it by 
default. (Note: Some Linuxes only include a base Python install. On Ubuntu, 
for instance, you may need to run `sudo apt-get install python-json` or 
`sudo apt-get python-cjson` to get one of the libraries.)

Usage
-----
The library is designed to be mostly transparent in usage. You simply 
extend the XML/JSON RPCHandler class from either the tornadorpc.xml or 
the tornado.json library, resepectively, and pass that handler in to 
the Tornado framework just like any other handler. 

For any synchronous (normal) operation, you can just return the value
you want sent to the client. However, if you use any asynchronous
library (like Tornado's AsyncHTTPClient) you will want to call 
self.result(RESULT) in your callback. See the Asynchronous section
below for examples.

XML-RPC Example
---------------
To set up a simple XML RPC server, this is all you need:

	from tornadorpc.xml import XMLRPCHandler
	from tornadorpc import private, start_server

	class Handler(XMLRPCHandler):

	    def add(self, x, y):
	        return x+y

	    def ping(self, obj):
	        return obj
    
	    @private
	    def private(self):
	        #should not get called
	        return False

	start_server(Handler, port=8080)

The `@private` decorator is a way to ensure that it cannot be called 
externally. You can also create methods that start with an underscore `_` 
character, and they will be private by default. The `start_server` function 
is just an easy wrap around the default Tornado setup -- you can use these 
handlers just like you would any other Tornado RequestHandler. 

JSON-RPC Example
----------------
A JSON-RPC server would be started with the exact same syntax, replacing 
XMLRPCHandler with JSONRPCHandler. Here is an example of the JSON-RPC 
client with "dot-attribute" support:

	from tornadorpc.json import JSONRPCHandler
	from tornadorpc import private, start_server

	class Tree(object):

	    def power(self, base, power, modulo=None):
	        result = pow(base, power, modulo)
            return result
  
	    def _private(self):
	        # Won't be callable
	        return False

	class Handler(JSONRPCHandler):

	    tree = Tree()

	    def add(self, x, y):
	        return x+y

	    def ping(self, obj):
	        return obj

	start_server(Handler, port=8080)

To use this, you should be able to use either the JSON-RPC official 
implementation, or the jsonrpclib library (which you'd need for this to 
work anyway.) One of the benefits of the jsonrpclib is designed to be a 
parallel implementation to the xmlrpclib, so syntax should be very similar 
and it should be easy to experiment with existing apps.

An example of client usage would be:

    from jsonrpclib import Server
    server = Server('http://localhost:8080')
    result = server.tree.power(2, 6)
    # result should equal 64

Asynchronous Example
--------------------
To indicate that a request is asynchronous, simply use the "async" 
decorator, and call "self.result(RESULT)" in your callback. Please note
that this will only work in the RPCHandler methods, not in any sub-tree
methods since they do not have access to the handler's result() method.

Here is an example that uses Tornado's AsyncHTTPClient with a callback:

    from tornadorpc import async
    from tornadorpc.xml import XMLRPCHandler
    from tornado.httpclient import AsyncHTTPClient

    class Handler(XMLRPCHandler):
        
        @async
        def external(self, url):
            client = AsyncHTTPClient()
            client.fetch(url, self._handle_response)
            
        def _handle_response(self, response):
            # The underscore will make it private automatically
            # You could also use @private if you wished
            # This returns the status code of the request
            self.result(response.code)

Debugging
---------
There is a `config` object that is available -- it will be expanded as time 
goes by. Currently, it supports two options: `verbose` and `short_errors`, 
both of which default to True. The `verbose` setting just specifies whether 
you want to print out results to the terminal (automatically on, you'll 
probably want to turn that off for production, WSGI deployment, etc.) and 
the `short_errors` option determines whether to print just the last few 
lines of the traceback (if set to True, default) or print the full traceback. 
Once the logging mechanism is in place, the `short_errors` configuration 
element will apply to that as well.

The default error look something similar to this:

	JSON-RPC SERVER AT http://localhost:8484
	---------------
	ERROR IN messup
	---------------
	Traceback (most recent call last):
	  File "test.py", line 20, in messup
	    return doesntexist['bad_key']
	NameError: global name 'doesntexist' is not defined

To change the configuration, look over the following:

	import tornadorpc
	tornadorpc.config.verbose = False
	tornadorpc.config.short_errors = False
	# or...
	from tornadorpc import config
	config.verbose = False
	config.short_errors = False
    
Tests
-----
To run some basic tests, enter the following in the same directory that
this README is in:

    python run_tests.py
    
This will test a few basic utilites and the XMLRPC system. If you wish
to test the JSONRPC system, run the following:
    
    python run_tests.py --json
    
TODO
----
* Add unit tests
* Add logging mechanism
* Add proper HTTP codes for failures
* Optimize
