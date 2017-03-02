# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
A small simple port of aioyoyo to use asyncio instead of its original
threading client. Creating an IRCClient instance will create the protocol
instance.

To start the connection run IRCClient.connect(); (coroutine)
"""

import logging

from .oyoyo.parse import *
from .protocol import ClientProtocol

from aioyoyo.oyoyo.cmdhandler import IRCClientError


class IRCClient(object):
    def __init__(self, loop, address=None, port=None, protocol=ClientProtocol):
        """Takes the event loop, a host (address, port) and if wanted
        an alternate protocol and be defined. By default will use the
        ClientProtocol class, which just uses the IRCClient's tracebacks"""
        self.loop = loop
        self.host = (address, port)
        self.address = address
        self.port = port
        self.protocol = protocol(self)

        self.logger = logging.getLogger("aioyoyo")
        self.logger.setLevel(logging.INFO)

    async def connect(self):
        await self.loop.create_connection(lambda: self.protocol, self.address, self.port)

    async def connection_made(self):
        logging.info('connecting to %s:%s' % self.host)

    async def data_received(self, data):
        logging.info('received: %s' % data)

    async def connection_lost(self, exc):
        logging.info('connection lost: %s' % exc)

    async def send(self, *args):
        bargs = []
        for arg in args:
            if isinstance(arg, str):
                bargs.append(arg.encode())
            elif isinstance(arg, bytes):
                bargs.append(arg)
            else:
                raise IRCClientError('Refusing to send one of the args from provided: %s'
                                     % repr([(type(arg), arg) for arg in args]))

        msg = b" ".join(bargs)
        await self.protocol.send_raw(msg + b"\r\n")
        logging.info('---> send "%s"' % msg)

    async def send_msg(self, message):
        await self.protocol.send(message)

    async def send_raw(self, data):
        await self.protocol.send_raw(data)

    async def close(self):
        logging.info('close transport')
        self.protocol.transport.close()


class CommandClient(IRCClient):
    """IRCClient, using a command handler"""
    def __init__(self, loop, cmd_handler, address=None, port=None, protocol=ClientProtocol, **kwargs):
        """Takes a command handler (see oyoyo.cmdhandler.CommandHandler)
        whose attributes are the commands you want callable, for example
        with a privmsg cmdhandler.privmsg will be awaited with the
        appropriate *args, decorate methods with @protected to make it
        uncallable as a command"""
        IRCClient.__init__(self, loop, address=address, port=port, protocol=protocol, **kwargs)
        self.command_handler = cmd_handler(self)

    async def data_received(self, data):
        prefix, command, args = parse_raw_irc_command(data)
        await self.command_handler.run(command, prefix, *args)
