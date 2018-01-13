import timeit
import binascii

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

da = open("speed.py", "rb").read()

def test_speed():
    return crc32(da).hexdigest()

s = timeit.timeit("test_speed()", setup="from __main__ import test_speed", number=10)
print(s)