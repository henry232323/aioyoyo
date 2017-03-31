#!/usr/bin/python3
# Copyright (c) 2016-2017, henry232323
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
"""A basic subclass of asyncio.Protocol using a buffer (for combined / split
irc messages, calls self.client.x for all callback events"""
import asyncio

class ClientProtocol(asyncio.Protocol):
    """Default protocol, forewards all events to the client"""
    def __init__(self, client):
        self.client = client
        self.buffer = bytes()
        self.sockname = None
        self.transport = None

    def connection_made(self, transport):
        """Called on a successful connection, calls client.connection_made"""
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        asyncio.ensure_future(self.client.connection_made())
        
    def connection_lost(self, exc):
        """Called on a lost connection, calls client.connection_lost"""
        asyncio.ensure_future(self.client.connection_lost(exc))
        
    def data_received(self, data):
        """Called when data is received, calls client.data_received"""
        self.buffer += data
        pts = self.buffer.split(b"\n")
        self.buffer = pts.pop()
        for el in pts:
            asyncio.ensure_future(self.client.data_received(el))

    async def send(self, message):
        """Send an unencoded message to the server, will be encoded"""
        self.transport.write(message.encode())

    async def send_raw(self, data):
        """Send raw bytes to the server"""
        self.transport.write(data)