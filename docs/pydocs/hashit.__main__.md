  ---------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------
   \                                                         [index](.)\
   \                                                         [/home/javad/Dropbox/playground/hashit/hashit/\_\_main\_\_.py](file:/home/javad/Dropbox/playground/hashit/hashit/__main__.py)
  **[hashit](hashit.html).\_\_main\_\_** (version 3.3.3a0)   
  ---------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------

`Command line program for hashit   this module "__main__" contains all the code for argparsing, running and anything needed for an command lin application such as hashit.   it uses argc another package by me, but i am considering switching to argparse`

 \
**Modules**

`      `

 

  -------------------------- -------------------- ---------------- ------------------------
  [hashlib](hashlib.html)\   [json](json.html)\   [os](os.html)\   [random](random.html)\
  -------------------------- -------------------- ---------------- ------------------------

 \
**Functions**

`      `

 

[**Exit**]{#-Exit} = exit(...)
:   `exit([status])   Exit the interpreter by raising SystemExit(status). If the status is omitted or None, it defaults to zero (i.e., success). If the status is an integer, it will be used as the system exit status. If it is another kind of object, it will be printed and the system exit status will be one (i.e., failure).`

<!-- -->

[**config**]{#-config}(argv)
:   `Sets argvs' config and commands`

<!-- -->

[**main**]{#-main}(args=None)
:   `Main function with error catching, can force-exit with os._exit(1)   this main function calls main_() and cathes any error while giving the user a "pretty" error.`

<!-- -->

[**main\_**]{#-main_}(args=None)
:   `Main function which is the cli parses arguments and runs appropriate commands`

<!-- -->

[**walk**]{#-walk}(goover)
:   `Goes over a path an finds all files, appends them to a list and returns that list`

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
**LINUX\_LIST** = \['Mythbuntu', 'Mac OS X', 'Debian Pure Blend', 'RPM',
'Symphony OS', 'Astra Linux', 'Emdebian Grip', 'Russian Fedora Remix',
'Secure-K', 'Knopperdisk', 'Mobilinux', 'touchscreen', 'MX Linux',
'NepaLinux', 'fli4l', 'Nix', 'Ubuntu Mobile', 'primary', 'Fedora Core',
'ChromeOS', ...\]\
**\_\_algorithms\_\_** = \['sha', 'DSA', 'md4', 'md5', 'sha1', 'crc32',
'sha384', 'sha512', 'sha224', 'sha256', 'DSA-SHA', 'blake2s', 'blake2b',
'whirlpool', 'ripemd160', 'dsaWithSHA', 'dsaEncryption',
'ecdsa-with-SHA1'\]\
**\_\_license\_\_** = 'MIT, Copyrigth (c) 2017-present Javad Shafique'

 \
**Author**

`      `

 

Javad Shafique
