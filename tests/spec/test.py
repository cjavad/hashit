import timeit
import binascii
import sys
import json
sys.path.insert(0, "..")
import hashit

# create a crc32 hash
def hex_crc32(buf):
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return ("%08X" % buf).lower()


# final class
class crc32:
    def __init__(self, data = b''):
        self.data = data

    def update(self, data):
        self.data += data

    def hexdigest(self):
        return hex_crc32(self.data)

da = str()

def test_speed():
    return crc32(da).hexdigest()

'''
s = timeit.timeit("test_speed()", setup="from __main__ import test_speed", number=10)
print(s)
'''

def collision():
    crc = lambda d=b'': hashit.new("crc32", d).hexdigest()
    done = {}

    for n in range(1000**3*4 + 1):
        n = str(n)
        h = crc(n.encode())
        if h in done:
            print("ERROR collision found in CRC32", h, n, "and", done[h])
        else:
            try:
                done[h] = n
            except MemoryError:
                done.clear()


if __name__ == "__main__":
    da = open("speed.py", "rb").read()
    collision()

'''
back = []
data = open("./res/crc_hashcollisions.txt", "r").readlines()

for l in data:
    l = l.split(" ")
    back.append(' '.join([l[0] + ":", l[1], l[2]]))

open("file.yaml", "w").writelines(back)
'''