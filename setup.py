from setuptools import setup
from hashit.version import __version__

LONG_DES = """
Hashit is an hashing program which can be uses to hash and verify muliple files on a system.
I got the idea from an ubuntu iso image which have this hash table, so i got the idea to make
such a program using python.

In version 1.2.2 i fixed some issues with print and if/else

Works with python2 and python3.
"""

setup(
    name = "hashit",
    author = "Javad Shafique",
    author_email = "javadshafique@hotmail.com",
    version=__version__,
    license="MIT"
    entry_points = {
        "console_scripts":[
            "hashit = hashit:main"
        ]
    },
    packages=["hashit"],
    description = "Hashing Application",
    long_description = LONG_DES,
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ]
)
