from setuptools import setup

# Get the long description from the README file
long_description = """Aioyoyo
A port of oyoyo to Asyncio for Python 3.5+

Uses Asyncio instead of its original threading client. Creating an IRCClient instance will create the protocol instance.
To start the connection run IRCClient.connect(); (coroutine)

Uses oyoyo from [illuminatedWax](https://github.com/illuminatedwax)'s Pesterchum, slightly modified
"""

setup(
    name='aioyoyo',
    version='1.2.2',
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
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='IRC Asyncio',
    packages=["aioyoyo", "aioyoyo.oyoyo"],
)
