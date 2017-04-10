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
from setuptools import setup

long_description = """Aioyoyo
A port of oyoyo to Asyncio for Python 3.5+

Uses Asyncio instead of its original threading client. Creating an IRCClient instance will create the protocol instance.
To start the connection await IRCClient.connect();

Uses oyoyo from [illuminatedWax](https://github.com/illuminatedwax)'s Pesterchum, slightly modified
oyoyo is an IRC library for Python, this project makes it completely asynchronous, with event callbacks
"""

setup(
    name='aioyoyo',
    version='1.2.4',
    description='An Asyncio oyoyo port',
    long_description=long_description,
    url='https://github.com/henry232323/aioyoyo',
    author='henry232323',
    author_email='henry@rhodochrosite.xyz',
    license='GPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='IRC Asyncio',
    packages=["aioyoyo", "aioyoyo.oyoyo"],
)
