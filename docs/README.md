[![](../icon.png)](https://pypi.org/project/hashit) 
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

## Usage
see [docs/usage.md](usage.md)


## Installing

I would recommend installing it from pypi like this
    
    pip(3) install hashit

But you can also install it from snap

    snap install hashit (--devmode or --classic is recommend)

## Technical Notes
```
There where a memory leak in the check function which caused wrong hashes to be resolved from my observatitions it
has something to do with pythons generators, i fixed it by added an read-all mode (normal) and made it default in 
the check function and other systems to, but by given the application ```-m``` you will enable the generator for
the initial hash, which so far hasn't shown any memory leaks but the check function will still be running on the default
read-all mode.

The check function works by detect/selecting hashtype and fileformat then applying the data by creating indexes for diffrent values
such as the hash, path and filesize. These indexes can then be used on the lists we create from the line in the file using the fileformats̈́
parser.
```

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

## Notes:

- I interpet N/a as None At All because i can
- The dist.zip (not in repo) contains all the old versions of the software
- Detect only works for a few selected algoritms