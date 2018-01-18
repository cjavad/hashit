|Snap Status| Project is hosted on
`pypi <https://pypi.org/project/hashit/>`__

Hashit is an hashing program which can be uses to hash and verify
muliple files on a system. I got the idea from an ubuntu iso image which
have this hash table, so i got the idea to make such a program using
python.

I also found that the linux 'standard' hashing commands was named like this:
    - md5sum
    - sha1sum
    - sha256sum
    - cksum
    - sum
    
hashname + sum, which i thougth was a pretty lame naming convention.

Notice:
~~~~~~~

some hashes as blake2b and blake2s is not supported in python2 and all
shake hashes is disabled for now

i would recommend python3 for this program as its version of hashlib
supports sha3 (Keccak)

Usage
--------------

Command line wise

.. code:: bash

    (python3 -m) hashit [options] $path

From python you can do it like this

.. code:: py

    from hashit import hashlib, blockIter, hashIter, hashFile, new

    file = open("somefile", "rb")

    """ memory efficent generator """
    hash1 = hashIter(blockIter(file, blocksize=65536), hasher=new("md5"), ashexstr=True)

    """ easy access """
    hash2 = hashFile("somefile", new("md5"), False)  # enable memory effienct generator (False)

    assert hash1 == hash2
    print(hash1, hash2)

Changelog
--------------

::

    3.1.2-3.1.3 - fixed this document

    3.1.0 - A bunch of bugfixes in comparing of hashes, shake and more

    3.0.2 - Fixed size positioning

    3.0.1 - Added --size option that allows the program to check file sizes to

    3.0.0 - New release, added tests full color-support and CRC32 hashing! (Also added an -a option)

    2.3.0 - Fixed a bunch of code, made it faster better more powerful. Full support for sfv and more!

    2.1.3 - Fixed detect bugs added unit tests and some fixes

    2.1.2 - Done with detect.py working hash detection

    2.1.1 - Some more bugfixed, started working on detect.py

    2.1.0 - Updated to support newest version of argc

    2.0.1 - Bugfixes

    1.2.0 - Full Release

    1.1.0 - Added support for python2 and 

    1.0.2 - Double exits' fixed

    1.0.1 - Fixed printing bug

    1.0.0 - Major version

    0.0.3 - Added documentation and license

    0.0.2 - Fixing script bugs

    0.0.1 - Initial release, ready for use

Works with python2 and python3.

.. |Snap Status| image:: https://build.snapcraft.io/badge/JavadSM/hashit.svg
   :target: https://build.snapcraft.io/user/JavadSM/hashit
