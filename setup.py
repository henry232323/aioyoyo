from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aioyoyo',
    version='1.1.0',
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