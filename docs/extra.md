---
layout: default
---

## Extra

One of the ways i have setup hashit, is that it's very flexible which means
that you the user can add change the way the program behaves quite easily

This is achived by making the program needing and global config which in this case
is the dict ```GLOBAL``` and with it you can translate, change and command this program.

Some notes before i go into details:
- The OSError Error message for linux need to include the ```{}``` for the .format to insert a list of linux distos

Ok the load() function from ```hasht.__init__``` which also is in ```hashit.__main__``` is what you'll need
for all your plugin loading needs.

To use this and the GLOBAL config all you need to do is to create your own little python file
lets call it hit.py

```py

from hashit.__main__ import main, load, new, GLOBAL

# set some config
GLOBAL["DEFAULTS"]["DETECT"] = True # always detect
GLOBAL["DEFAULTS"]["RECURS"] = False # dont use -r by default
GLOBAL["MESSAGES"]["FILE_NOT"] = "I guess that file was like... Oh No" # insert sarcatic error-messages


class my_hash_api:
    name = "hash_3-2-1"
    def __init__(self, data=b''):
        self.data = data

    def update(self, data):
        self.data += data

    def digest(self):
        # calculate hash
        return 2312319230193912123

    def hexdigest(self):
        return hex(self.digest())

load(my_hash_api) # loads' hash_3-2-1
# test it if you want to
# assert new("hash_3-2-1", b'My Custom Hash').hexdigest() == "0x20170216b303493b"

# and then add a the executable code
if __name__ == "__main__":
    main()
```
and then you can call the program as such
```python3 hit.py -H hash_3-2-1```

see [plugins](plugins.md) for more about the loading of plugins

## GUI
[](#gui)

One of my goals with this project is to create an easy-to-use gui, which i have yet to acomplish
for now see [this](../tests/spec/gui.py) file for an example of how to create an gui for hashit

[back](index.md)
