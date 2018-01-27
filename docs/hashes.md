---
layout: default
---

## Supported

List off all supported hashes for all versions

For all versions crc32 is supported

For python2 is

- md4
- md5
- sha
- sha1 ('DSA-SHA', 'ecdsa-with-SHA1', 'dsaEncryption', 'DSA', 'dsaWithSHA')
- sha224
- sha256
- sha384
- sha512
- ripemd160
- whirlpool

For python3 is all from python2 and more:

- blake2s
- blake2b
- sha3_224
- sha3_256
- sha3_384
- sha3_512

## Experimental

And for python3 a special syntax for the shake hash
where by default shake-256 is used like this
```shake_(length)```

so 

```bash
$ touch file
$ python3 -m hashit -H shake_2 file -sp
49b9 ./file
```

[back](index.md)
