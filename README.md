# oyoyo-asyncio
A port of oyoyo to Asyncio for Python 3.5

Uses Asyncio instead of its original threading client. Creating an IRCClient instance will create the protocol instance.
To start the connection run IRCClient.connect(); (coroutine)

Uses oyoyo from [illuminatedWax](https://github.com/illuminatedwax)'s Pesterchum, slightly modified
