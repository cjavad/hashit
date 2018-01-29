---
layout: default
---

[![](https://raw.githubusercontent.com/JavadSM/hashit/master/icon.png)](https://pypi.org/project/hashit) 
# Hashit, an hashing application

Hashit is an command line hashing application that supports a large varity of fileformats and hashing algorithms
written in python(3) for hashing an verifing files.

File Formats it supports:

- Default: where ```hash [size] filename```
    * used by md5sum

- Simple File Verification ```filename hash [size]```
    * popular checksum file format

- BSD-tag style ```hashname (filename) = hash [size]```
    * output from bsd systems hashing commands

One of the reasons i created this program was because i thougth (from README.rst) that the current naming convention for
hashing and file verification tools on debian based systems (they did better on bsd but still) where seriosly inefficent
by seperating each hash into a different tool (yes i am aware of that these tools are implemented in C and making them into one program could most likely also cause the same kind of confusion) so hashit ships with all hash functions in one program/command where md5 is the default.

See [docs/hashes.md](hashes.md) for the diffrent types of hashes supported

[](#usage)
## Usage
see [docs/usage.md](usage.md)


[](#installing)
## Installing

I would recommend installing it from pypi like this
    
    pip(3) install hashit

But you can also install it from snap

    snap install hashit (--devmode or --classic is recommend)

## Technical Notes
[](#technical)

There where a memory leak in the check function which caused wrong hashes to be resolved from my observatitions it
has something to do with pythons generators, i fixed it by added an read-all mode (normal) and made it default in 
the check function and other systems to, but by given the application ```-m``` you will enable the generator for
the initial hash, which so far hasn't shown any memory leaks but the check function will still be running on the default
read-all mode.

The check function works by detect/selecting hashtype and file format then applying the data by creating indexes for diffrent values
such as the hash, path and filesize. These indexes can then be used on the lists we create from the line in the file using the file formats
parser.

Due to some interface problems with snap, is it not posible to access devices than home and external drives. therefore i would recommend you to install it in --devmode but if you want you can also use classic. (Bypass: use sudo)

Due to the way exclude works it is not needed to use a wildcard '*' to exclude specific extentions for that just to '.ext'.
it works by doing: 
```py
if 'exclude-string`' in 'path':
    remove_from_list('path')
```

### Extra, see [extra](extra.md) for more

>
>  The hash-classes are built like so
>  all classes added needs this kind of
>  api due to compatibility. See [plugins](plugins.md) for more
> 
>```py
>class hashname:
>    name = "hashname"
>
>    def __init__(self, data=b''):
>        self.data = data
>    
>    def update(self, data=b''):
>        self.data += data
>
>    def copy(self):
>        # pass data on
>        return hashname(self.data)
>
>    def digest(self):
>        # generate hash
>        return GENERATED_HASH
>
>    def hexdigest(self):
>        # return as hex
>        G_HASH = self.digest()
>        return convert_to_hex(G_HASH)
>```

## Links
[](#links)
[extra](extra.md) how to setup hashit (plugins & config)

[pydocmd](pydoc.md) generated with pydocmd

[pydocs](pydocs/hashit.html) generated with pydocs

## Notes:
[](#notes)

- I interpet N/a as None At All because i can
- The dist.zip (not in repo) contains all the old versions of the software
- Detect does not work with shake due to its integration
- I would not recommend using -S --size because then you will have to specify it everytime you check
- Detect format benchmarks (using timeit on python3 ubuntu):
    * BSD: 7-5 seconds (10**6)
    * SFV: 4.2 seconds (10**6)
    * N/A: 2.4 seconds (10**6)
