# Aioyoyo
[https://img.shields.io/pypi/v/aioyoyo.svg](https://pypi.python.org/pypi/aioyoyo)
[https://img.shields.io/pypi/l/aioyoyo.svg](https://pypi.python.org/pypi/aioyoyo)
[https://img.shields.io/pypi/pyversions/aioyoyo.svg](https://pypi.python.org/pypi/aioyoyo)
<br />
A port of the Python IRC library oyoyo to Asyncio for Python 3.5+
A Python asyncio IRC library

Uses Asyncio instead of its original threading client. Creating an IRCClient instance will create the protocol instance.
To start the connection run IRCClient.connect(); (coroutine)

Uses oyoyo from [illuminatedWax](https://github.com/illuminatedwax)'s [Pesterchum](https://github.com/illuminatedwax/pesterchum/tree/master/oyoyo), slightly modified
