"""Extra functions and classes for hashit"""
import binascii

# create a crc32 hash
def hex_crc32(buf):
    """Hashes binary data with crc32 and returns hex"""
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return ("%08X" % buf).lower()


# final class
class Crc32:
    """This class is an api for the crc32 function that is compatible with mor"""
    def __init__(self, data=b''):
        """init class, creates data""" 
        self.name = "crc32"
        self.data = data

    def update(self, data):
        """Update self.data with new data"""
        self.data += data

    def digest(self):
        """Digest as int"""
        return binascii.crc32(self.data) & 0xFFFFFFFF

    def hexdigest(self):
        """Digest as hex"""
        return hex_crc32(self.data)
