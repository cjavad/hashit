"""Extra functions and classes for hashit"""
import binascii
import hashlib

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

    def update(self, data=b''):
        """Update self.data with new data"""
        self.data += data

    def digest(self):
        """Digest as int"""
        return binascii.crc32(self.data) & 0xFFFFFFFF

    def hexdigest(self):
        """Digest as hex"""
        return hex_crc32(self.data)

# class for shake hash
class shake:
    def __init__(self, hashname, data=b''):
        """Init class create hasher and data"""
        if hashname[:5] == "shake":
            self.hash = hashlib.shake_256()
            self.name = hashname
            self.data = data
            self.length = int(hashname.split("_")[1])
        else:
            raise ValueError

    def update(self, data=b''):
        """Update self.data with new data"""
        self.data += data

    def digest(self, length=None):
        """Digest binary"""
        length = length or self.length
        return self.hash.digest(length)
    
    def hexdigest(self, length=None):
        """Digest hex"""
        length = length or self.length
        return self.hash.hexdigest(length)
