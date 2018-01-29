.. image:: https://build.snapcraft.io/badge/JavadSM/hashit.svg
   :target: https://build.snapcraft.io/user/JavadSM/hashit

Project is hosted on `pypi <https://pypi.org/project/hashit/>`__

.. image:: icon.png
   :target:  https://github.com/javadsm/hashit
   :align: right

Hashit, an hashing application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


What is this magic (hashing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
..

   Hashing - The Greatest Idea In Programming

A quote from `here <http://www.i-programmer.info/babbages-bag/479-hashing.html>`__, which i think sums up the hole thing pretty well.
Even though, that stament is purely opinion based, i still thing there is some weigth in it, because you can do so many things with "hashing".
First of all the concept of hashing is that you can, with an matematical algorithm generate a string that is unique to that piece of data, but
you cannot turn that string into the data again, this is done by generating a string which size is constant (or at least not changing from data to data).
And this is actually extreamlly useful, because this enables you to generate a string that is smaller than the original while still being totally unique,
this can be using in databases for bigdata where you can create a lookup table without needing to use the hole amount of data, it can also be used to verify data
such as passwords and file-checksums, which by the way is what this program is. I use the standard python hashes libary hashlib, which comes with most versions of
python, some function like crc32 are from other libaries, i use these to hash some files and store the results in a checksum-file, which can be read back and check
if the files have changed, this is very important when it comes to packaging, and other critical files, were one must be absoulutly sure that the file has not
been changed, because if it has it could be due to corruption or infection of some kind of malware, so by making sure that the package is the same as the original.
Some file systems use these hashes to make sure that the files havn't been alteret externally.

For more see `docs/hashes <docs/hashes.md>`__ and the `wikipedia page <https://en.wikipedia.org/wiki/Hash_function>`__


Background
~~~~~~~~~~

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

some hashes as blake2b and blake2s is not supported in python2.

I would recommend python3 for this program as its version of hashlib
supports sha3 (Keccak)

And for compatibly reasons does detect not work for sha3 yet. so basicly to many confusions between sha2 and sha3

BSD can be useful with the -A --append because then multiple diffrent hashtypes can be stored
in the same file, good for multi-sized file validation. (remember -m)


Usage
--------------

See `docs/usage <docs/usage.md>`__

Changelog
--------------

    3.3.8 - Added more documentation and added sha3 (Keccak) support for detect, also added -e --exclude that can exclude dirs from list

    3.3.7 - Refractored the hashit.check code so you can now use it from python! (see `docs/extra.md#gui <docs/extra.md#gui>`__ for an example)

    3.3.6 - Minor bugfixes and removed -a, added -p --page for a help-page in the terminal for the python-api

    3.3.5 - hashit now supports a list of files such as the wildcard in linux, and can detect if that element is a directory

    3.3.4 - Bugfixes and more, fixed parsers added some benchmarks and fixing some more of the snap-related issues

    3.3.3 - Full release

    3.3.3a3 - Extended Configs working on homepage and docs

    3.3.3a2 - Added --trace and fixed some of the issues with detect and argparse

    3.3.0a1 - removed argc depend, using argparse

    3.3.0a0 - Fixing snap releated issues

    3.3.1 - Fixed bug in windows where \ would not be replaced by / in hashit.fixpath

    3.3.0 - Added BSD Style output and check format detection. Also an -s option that can hash a piece of text see `docs <https://github.com/JavadSM/hashit/blob/master/docs/>`__ for more

    3.2.1 - ReRelease for snap

    3.2.0 - Full support for snap

    3.1.5 - Skipped 3.1.4 cause i have been renaming varibles, cleaning code and improving performance.

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
