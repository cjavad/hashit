.. image:: https://build.snapcraft.io/badge/cjavad/hashit.svg
   :target: https://build.snapcraft.io/user/cjavad/hashit

Project is hosted on `pypi <https://pypi.org/project/hashit/>`__ and `launchpad <https://launchpad.net/python3-hashit>`__

.. image:: img/icon.png
   :target:  https://github.com/cjavad/hashit
   :align: right

Hashit, an hashing application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: img/demo.gif
    :target: https://asciinema.org/a/TZQCel3DNy2sCWOFBtQcqVMMM
    :alt: asciinema demo usage.

Description
~~~~~~~~~~~
Hashit, is an hashing application used as an verification tool, intendet to replace the "standard" linux hashing utilities such as
md5sum, sha1sum and so on. One of the main reasons why this program was develop was to create an easy-to-use command line tool for 
newcomers and professionals alike to hash/verify files and other data. For more see our homepage at `cjavad.github.io/hashit <https://cjavad.github.io/hashit>`__ 

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
See `debian/changelog <changelog>`__


Works with python2 and python3. (python3 is recommended)


.. image:: https://badges.gitter.im/cjavad/hashit.svg
   :alt: Join the chat at https://gitter.im/cjavad/hashit
   :target: https://gitter.im/cjavad/hashit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge