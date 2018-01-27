---
layout: default
---

With the new release, i have added support for loading thirdparty hashfunction to hashit via load() and GLOBAL
basicly it adds a new entry to GLOBAL.EXTRA with its' name and class. The way these plugins work are quite simple,
all it needs is a hashlib compatible api as such:
> plugin.py

[//]: # (Blank Comment as seperator)
```py
class thirdpartyhash:
    """Api for another hashfunction"""
    name = "hashname" # define now or in self.name
    
    def __init__(self, data=b''):
        # self.name = "hashname"
        self.data = data

    def update(self, data):
        self.data += data

    def digest(self):
        # use whatever function you need
        return hashname(self.data).raw
    
    def hexdigest(self):
        # convert output to hex
        return convert_to_hex(self.digest())
    
    # the copy function is optional, not needed
    # but is still a part of the api
    def copy(self):
        return thirdpartyhash(self.data)


```
> hashit (.py) a new executable

[//]: # (Blank Comment as seperator)
```py
import sys
from hashit.__main__ import main, load
from plugin import thirdpartyhash as tph

load(tph)
main(sys.argv[1:])

```
or
> pythonprogram.py your own program using hashits' hashing functions

[//]: # (Blank Comment as seperator)
```py
from hashit import new, load, hashFile
from plugin import thirdpartyhash as tph

load(tph)
hasher = new("hashname")
print(hashFile("somefile.ext", hasher, True))
```
[back](index.md)
