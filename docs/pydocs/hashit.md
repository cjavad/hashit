  ------------ -------------------------------------------------------------------------------------------------------------------------------
   \           [index](.)\
   \           [/home/javad/Dropbox/playground/hashit/hashit/\_\_init\_\_.py](file:/home/javad/Dropbox/playground/hashit/hashit/__init__.py)
  **hashit**   
  ------------ -------------------------------------------------------------------------------------------------------------------------------

`hashit module for hashit command is contaning all the code for hashit   hashit is an hashing application which main purpose is to replace all the 'default' hashing commands that comes with linux and also provide a usable hashing program for windows hence the choice of using python. while hashit supports both python 2 and 3 i would strongly recommend using python3 because that python3 comes with a newer version of hashlib and therefore many new hash-functions, altough it is posible to add these into python2 with the load() function which acts like a 'connecter' and enables hashit to use third-party hashing-functions as long as the have the same api as specified in docs/README.md    MIT License                                                                         Copyright (c) 2018 Javad Shafique                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:   The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.   NO ONE CAN CLAIM OWNERSHIP OF THIS "SOFTWARE" AND ASSOCIATED DOCUMENTATION FILES.`

 \
**Package Contents**

`      `

 

  --------------------------------------- ------------------------------------- ----------------------------- ---------------------------------
  [\_\_main\_\_](hashit.__main__.html)\   [detection](hashit.detection.html)\   [extra](hashit.extra.html)\   [version](hashit.version.html)\
  --------------------------------------- ------------------------------------- ----------------------------- ---------------------------------

 \
**Functions**

`      `

 

[**Exit**]{#-Exit} = exit(...)
:   `exit([status])   Exit the interpreter by raising SystemExit(status). If the status is omitted or None, it defaults to zero (i.e., success). If the status is an integer, it will be used as the system exit status. If it is another kind of object, it will be printed and the system exit status will be one (i.e., failure).`

**\_\_help\_\_** *lambda* help\_command

[**blockIter**]{#-blockIter}(afile, blocksize=65536)
:   `Will create a generator for reading a file`

<!-- -->

[**bsd2str**]{#-bsd2str}(bsdstr, size=False)
:   `Parses a bsd compatible string to an array`

<!-- -->

[**bsd\_tag**]{#-bsd_tag}(file\_hash, file\_path, hashname)
:   `Formats string in a bsd style format`

<!-- -->

[**check**]{#-check}(path, hashit, useColors=False, be\_quiet=False, detectHash=True, sfv=False, size=False, bsdtag=False)
:   `Will read an file which have a SFV compatible checksum-file or a standard one and verify the files checksum`

<!-- -->

[**choose\_hash**]{#-choose_hash}(hash1, hashit)
:   `Uses detect.decect to identify hashes with a high accuracy but when there if some issues it will take user input.`

<!-- -->

[**detect\_format**]{#-detect_format}(s)
:   `Autodetect hash format, by checking the length and what it contains`

<!-- -->

[**eprint**]{#-eprint}(\*args, \*\*kwargs)
:   `Prints to stderr usefull for warnings and error messages`

<!-- -->

[**fixpath**]{#-fixpath}(path)
:   `Returns full path and supports snap`

<!-- -->

[**hashFile**]{#-hashFile}(filename, hasher, memory\_opt=False)
:   `hashFile is a simple way to hash files using diffrent methods`

<!-- -->

[**hashIter**]{#-hashIter}(bytesiter, hasher, ashexstr=True)
:   `Will hash the blockIter generator and return digest`

<!-- -->

[**load**]{#-load}(hashclass)
:   `Add hashes to GLOBAL.EXTRA which is the dict that contains all the "extra" hash-functions such as Crc32, which allows external hashing algorithms to  be used as long as the have the same api as specified in docs/README.md   returns True/False based on whether or not the data is loaded`

<!-- -->

[**load\_all**]{#-load_all}(list\_of\_hashclasses)
:   `Just for it, a function that loads all plugins in a list`

<!-- -->

[**new**]{#-new}(hashname, data=b'')
:   `Custom hash-init function that returns the hashes`

<!-- -->

[**read\_sfv**]{#-read_sfv}(filename)
:   `Creates generator that reads and parses sfv compatible files using reader`

<!-- -->

[**reader**]{#-reader}(filename, mode='r', remove\_binary\_mark=True)
:   `Creates generator for an file, better for larger files not part of the MEMOPT`

<!-- -->

[**sfv\_max**]{#-sfv_max}(file\_hash, file\_path, longest, size='')
:   `calculates the amount of spaces needed in a sfv file`

<!-- -->

[**supports\_color**]{#-supports_color}()
:   `Returns True if the running system's terminal supports color, and False otherwise.`

 \
**Data**

`      `

 

**GLOBAL** = {'ACCESS': True, 'BLANK': (None, True), 'COLORS': {'GREEN':
'\\x1b\[0;32m', 'RED': '\\x1b\[0;31m', 'RESET': '\\x1b\[0m', 'YELLOW':
'\\x1b\[0;33m'}, 'DEFAULTS': {'APPEND': False, 'COLORS': True, 'DETECT':
None, 'HASH': 'md5', 'MEMOPT': False, 'QUIET': False, 'SIZE': False,
'STRIP': False}, 'DEVMODE': True, 'ERRORS': {'FileNotFoundError':
"Error, file seems to be missing calling systemd to confirm 'sure you
haved checked the MBR?'", 'OSError': {'END': 'JDK, so something happend
with your os, message: ', 'linux': 'So {} , to be continued...\\n',
'macos': 'Macos (Sierra+) and OSX (El Captain-) thank god for apples
naming', 'windows': 'Windows 10, windows 8(.1), windows 7 (sp\*),
wind...p\*), windows 98/95, windows NT \*. OK not that bad'},
'TypeError': 'Wrong type used (in cli-arguments) - please use a static
programming language'}, 'EXTRA': {'crc32': &lt;class
'hashit.extra.Crc32'&gt;}, 'HASH\_STR': 'Hello World!', 'MESSAGES':
{'CUR\_FORM': 'current format is', 'EMPTY\_CHK': 'checksum file is
empty', 'FAIL': 'FAILED', 'FILE\_NOT': 'File does not exist',
'HASH\_NOT': 'is not a valid hash', 'LOAD\_FAIL': 'Failed to load',
'MAYBE': 'Did you maybe mean:', 'OK': 'OK', 'PERM\_ERR': 'could not be
accessed', 'WORKS\_ON': 'is not guaranteed to work on your system',
...}, 'SNAP\_PATH': '/var/lib/snapd/hostfs', ...}\
**\_\_algorithms\_\_** = \['md5', 'DSA', 'md4', 'sha', 'sha1', 'crc32',
'sha384', 'sha512', 'sha256', 'sha224', 'blake2b', 'blake2s', 'DSA-SHA',
'ripemd160', 'whirlpool', 'dsaWithSHA', 'dsaEncryption',
'ecdsa-with-SHA1'\]\
**\_\_license\_\_** = 'MIT, Copyrigth (c) 2017-present Javad Shafique'\
**print\_function** = \_Feature((2, 6, 0, 'alpha', 2), (3, 0, 0,
'alpha', 0), 65536)\
**with\_statement** = \_Feature((2, 5, 0, 'alpha', 1), (2, 6, 0,
'alpha', 0), 32768)

 \
**Author**

`      `

 

Javad Shafique
