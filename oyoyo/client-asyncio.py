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
'''
A small simple port of oyoyo to use asyncio instead of its original
threading client. Creating an IRCClient instance will create the protocol
instance.

To start the connection run IRCClient.connect(); (coroutine)
'''

import asyncio
import logging

from protocol import ClientProtocol

from oyoyo.parse import *
from oyoyo.cmdhandler import IRCClientError

class IRCClient(object):
    def __init__(self, loop, host, protocol=ClientProtocol):
        '''Takes the event loop, a host (address, port) and if wanted
        an alternate protocol and be defined. By default will use the
        ClientProtocol class, which just uses the IRCClient's tracebacks'''
        self.loop = loop
        self.host = host
        self.protocol = protocol(self)

    async def connect(self):
        await self.loop.create_connection(lambda: self.protocol, self.host[0], self.host[1])        

    def connection_made(self):
        logging.info('connecting to %s:%s' % self.host)
        
    def data_received(self, data):
        logging.info('received: %s' % data)

    def connection_lost(self, exc):
        logging.info('connection lost: %s' % exc)

    def send(self, *args):
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
        self.protocol.transport.write(msg + b"\r\n")       
        logging.info('---> send "%s"' % msg)

    def close(self):
        logging.info('close transport')
        self.protocol.transport.close()

class CommandClient(IRCClient):
    '''IRCClient, using a command handler'''
    def __init__(self, loop, host, cmd_handler, commands, protocol=ClientProtocol):
        '''Takes a command handler (see cmdhandler.CommandHandler) and
        and commands, an object (module, class, etc) which has the attributes
        of the commands you want accessible, i.e. commands.privmsg will be called
        on a private message with appropriate *args'''
        IRCClient.__init__(self, loop, protocol, host)
        self.command_handler = cmd_handler(self, commands)

    def data_received(self, data):
        prefix, command, args = parse_raw_irc_command(data)
        self.command_handler.run(command, prefix, *args)
