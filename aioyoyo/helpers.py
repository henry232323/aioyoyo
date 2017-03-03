# Copyright (c) 2008 Duncan Fordyce
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
"""Contains helper functions for common IRC commands"""

import random

async def msg(cli, user, msg):
    """Send message `msg` to `user` with PRIVMSG command"""
    for line in msg.split('\n'):
        cli.send("PRIVMSG", user, ":%s" % line)

async def names(cli, *channels):
    """Send NAMES command, see source"""
    tmp = __builtins__['list'](channels)
    msglist = []
    while len(tmp) > 0:
        msglist.append(tmp.pop())
        if len(",".join(msglist)) > 490:
            tmp.append(msglist.pop())
            cli.send("NAMES %s" % (",".join(msglist)))
            msglist = []
    if len(msglist) > 0:
        cli.send("NAMES %s" % (",".join(msglist)))

async def channel_list(cli):
    """Send the LIST command"""
    cli.send("LIST")

async def kick(cli, handle, channel, reason=""):
    """KICK `handle` from `channel` with optional `reason`"""
    cli.send("KICK %s %s %s" % (channel, handle, reason))

async def mode(cli, channel, mode, options=None):
    """Send the MODE command to the given `channel` with optional `options`"""
    cmd = "MODE %s %s" % (channel, mode)
    if options:
        cmd += " %s" % (options)
    cli.send(cmd)

async def ctcp(cli, handle, cmd, msg=""):
    """Send CTCP command using PRIVMSG where `handle` is the user, `cmd` is the command and the optional `msg`"""
    cli.send("PRIVMSG", handle, "\x01%s %s\x01" % (cmd, msg))

async def ctcp_reply(cli, handle, cmd, msg=""):
    """Forewards ctcp_reply command to notice function with added CTCP formatting"""
    notice(cli, str(handle), "\x01%s %s\x01" % (cmd.upper(), msg))

async def msgrandom(cli, choices, dest, user=None):
    """Function for random responses"""
    o = "%s: " % user if user else ""
    o += random.choice(choices)
    msg(cli, dest, o)

def _makeMsgRandomFunc(choices):
    """Function factory given `choices`"""
    async def func(cli, dest, user=None):
        msgrandom(cli, choices, dest, user)
    return func

msgYes = _makeMsgRandomFunc(['yes', 'alright', 'ok'])
msgOK = _makeMsgRandomFunc(['ok', 'done'])
msgNo = _makeMsgRandomFunc(['no', 'no-way'])


async def ns(cli, *args):
    """Messages NickServ with space joined *args"""
    msg(cli, "NickServ", " ".join(args))

async def cs(cli, *args):
    """Messages ChanServ with space joined *args"""
    msg(cli, "ChanServ", " ".join(args))

async def identify(cli, passwd, authuser="NickServ"):
    """Send IDENTIFY command with `passwd`, default `authuser` is NickServ"""
    msg(cli, authuser, "IDENTIFY %s" % passwd)

async def quit(cli, msg='gone'):
    """Send quit command with optional message, defaults to  'gone'"""
    cli.send("QUIT :%s" % msg)
    cli._end = 1

async def user(cli, username, realname=None):
    """Sends USER command with given `username`, uses realname instead if given"""
    cli.send("USER", realname or username, cli.host, cli.host,
        realname or username)

_simple = (
    'join',
    'part',
    'nick',
    'notice',
    'invite',
)
def _addsimple():
    import sys
    def simplecmd(cmd_name):
        def f(cli, *args):
            cli.send(cmd_name, *args)
        return f
    m = sys.modules[__name__]
    for t in _simple:
        setattr(m, t, simplecmd(t.upper()))
_addsimple()

def _addNumerics():
    import sys
    from .oyoyo import ircevents
    def numericcmd(cmd_num, cmd_name):
        def f(cli, *args):
            cli.send(cmd_num, *args)
        return f
    m = sys.modules[__name__]
    for num, name in ircevents.numeric_events.items():
        setattr(m, name, numericcmd(num, name))

_addNumerics()

