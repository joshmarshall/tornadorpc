#!/usr/bin/env/python
"""
Copyright 2009 Josh Marshall 
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

   http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 
"""

import distutils.core

distutils.core.setup(
    name = "tornadorpc",
    version = "0.1",
    packages = ["tornadorpc"],
    author = "Josh Marshall",
    author_email = "catchjosh@gmail.com",
    url = "http://code.google.com/p/tornadorpc/",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    description = "TornadoRPC is a an implementation of both JSON-RPC " +
                  "and XML-RPC handlers for the Tornado framework.",
)
