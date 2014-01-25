#!/usr/bin/env/python

import setuptools

with open("README.md") as readme:
    long_description = readme.read()
    with open("README", "w") as pypi_readme:
        pypi_readme.write(long_description)

setuptools.setup(
    name="tornadorpc",
    version="0.1.1",
    packages=["tornadorpc"],
    author="Josh Marshall",
    install_requires=["tornado", "jsonrpclib"],
    author_email="catchjosh@gmail.com",
    url="http://code.google.com/p/tornadorpc/",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="TornadoRPC is a an implementation of both JSON-RPC "
        "and XML-RPC handlers for the Tornado framework.",
    long_description=long_description
)
