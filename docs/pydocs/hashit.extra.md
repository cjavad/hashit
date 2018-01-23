  --------------------------------- ---------------------------------------------------------------------------------------------------------------------
   \                                [index](.)\
   \                                [/home/javad/Dropbox/playground/hashit/hashit/extra.py](file:/home/javad/Dropbox/playground/hashit/hashit/extra.py)
  **[hashit](hashit.html).extra**   
  --------------------------------- ---------------------------------------------------------------------------------------------------------------------

`Extra functions and classes for hashit`

 \
**Modules**

`      `

 

  ---------------------------- -------------------------- -- --
  [binascii](binascii.html)\   [hashlib](hashlib.html)\      
  ---------------------------- -------------------------- -- --

 \
**Classes**

`      `

 

[builtins.object](builtins.html#object)

[Crc32](hashit.extra.html#Crc32)

[shake](hashit.extra.html#shake)

 \
[class **Crc32**]{#Crc32}([builtins.object](builtins.html#object))

`   `

`This class is an api for the crc32 function that is compatible with mor `

 

Methods defined here:\

[**\_\_init\_\_**]{#Crc32-__init__}(self, data=b'')
:   `init class, creates data`

[**copy**]{#Crc32-copy}(self)

[**digest**]{#Crc32-digest}(self)
:   `Digest as int`

<!-- -->

[**hexdigest**]{#Crc32-hexdigest}(self)
:   `Digest as hex`

<!-- -->

[**update**]{#Crc32-update}(self, data=b'')
:   `Update self.data with new data`

------------------------------------------------------------------------

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

<!-- -->

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

 \
[class **shake**]{#shake}([builtins.object](builtins.html#object))

`   `

`Top-level api for hashlib.shake `

 

Methods defined here:\

[**\_\_init\_\_**]{#shake-__init__}(self, hashname, data=b'')
:   `Init class create hasher and data`

[**copy**]{#shake-copy}(self)

[**digest**]{#shake-digest}(self, length=None)
:   `Digest binary`

<!-- -->

[**hexdigest**]{#shake-hexdigest}(self, length=None)
:   `Digest hex`

<!-- -->

[**update**]{#shake-update}(self, data=b'')
:   `Update self.data with new data`

------------------------------------------------------------------------

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

<!-- -->

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

 \
**Data**

`      `

 

**LINUX\_LIST** = \['Mythbuntu', 'Mac OS X', 'Debian Pure Blend', 'RPM',
'Symphony OS', 'Astra Linux', 'Emdebian Grip', 'Russian Fedora Remix',
'Secure-K', 'Knopperdisk', 'Mobilinux', 'touchscreen', 'MX Linux',
'NepaLinux', 'fli4l', 'Nix', 'Ubuntu Mobile', 'primary', 'Fedora Core',
'ChromeOS', ...\]
