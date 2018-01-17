from __future__ import print_function
import unittest, hashlib, sys, random, string
from binascii import unhexlify # python3 support
sys.path.insert(0, "..")
import hashit
import hashit.__main__

# NOTE THE TESTS REQUIRE A MD5-CHECKSUM of a file as a point of comparionsing

FILE = "LICENSE"
FILE_SUM = "3d205fb716c7c57732eb37c1e29d82d9"

# check sums for file
FILE_SUMS = {
    "DSA": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "DSA-SHA": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "blake2b": "196bf4efa6c8e77b019ce834ea2c5011349171b395792316e109eb7d123533ce1c0a56917c76437e2ee4e26f65d3b447326f6bb0244f89cef2c88b9ce58aeb35",
    "blake2s": "c9a393cb9b0683b360bc257aaba1e8b34644f1753c8e60d705b8c87b1c091575",
    "crc32": "ebd1a795",
    "dsaEncryption": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "dsaWithSHA": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "ecdsa-with-SHA1": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "md4": "6cfc8cbf106583427461e6d2e1e93d0d",
    "md5": "3d205fb716c7c57732eb37c1e29d82d9",
    "ripemd160": "2a217ec724b82bba4a96c32612e897ec60f91910",
    "sha": "f6982fc17ec8fd17a048ef56161f83bd114f7f0c",
    "sha1": "3ccefed5c16a412668222aae97f7e293c34779b4",
    "sha224": "342ef4f554e58c7df12790813abef77b44cf98120d12d55ff8ebee26",
    "sha256": "066b8c740c367994ab192f6e2eced1ba2d7cc68d35f62ae93a2f9cfed5e5db2a",
    "sha384": "e2ece4ba03fcec5bf73e49516a911924b754179279035fc57c3d03986ea744c6ab24319d9566fbee7a17255dd1f2a2d9",
    "sha512": "855010d939eab6711357e47158e349ccb3f582e115f0f7c790c1ed8a8e8589f4f3d4a02e9e3d57eb2f1952da2249290fcac613e42b08881bd44245dce9b3ff7d",
    "whirlpool": "385df6dafb57b4862d309481dc91001f468978bd506d724d04efb1461f631c5952b6b0bc7e85770434abd28dab2240fc26d05751f0c9eca1254cb11883cd3065"
}

class Test(unittest.TestCase):
    def test_hasher(self):
        file = open(FILE, "rb")
        data = file.read()

        for algo in hashit.__algorithems__:
            h1 = hashit.new(algo, data).hexdigest()
            h2 = hashit.hashFile(FILE, hashit.new(algo), True)
            self.assertEqual(h1, h2)
            self.assertEqual(h1, FILE_SUMS[algo])

        h1 = hashit.new("md5", data).hexdigest()
        self.assertEqual(h1, FILE_SUM)
        file.close()

    def test_detect(self):
        # generate data set
        ds = hashit.generate_data_set("Hallo", hashit.__algorithems__, hashit.new)

        # hash file three times
        h1 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashlib.md5())
        h2 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashlib.sha224())
        h3 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashlib.sha1())
        h4 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new("crc32"))

        # detect for three algorigthms
        cl1 = hashit.detect(h1, ds)
        cl2 = hashit.detect(h2, ds)
        cl3 = hashit.detect(h3, ds)
        cl4 = hashit.detect(h4, ds)

        # correct hash names
        correct1 = "md5"
        correct2 = "sha224"
        correct4 = "crc32"

        # md5 or md4
        self.assertTrue(correct1 in cl1.maybe)

        # only one left should be true
        self.assertTrue(correct2 in cl2.certain)
        self.assertTrue(correct4 in cl4.certain)
        # and if it is to check hash with it
        self.assertEqual(hashit.new(correct2, b'Hallo').hexdigest(), hashit.new(cl2.certain[0], b'Hallo').hexdigest())

        # for sha1 more options should be avaible
        self.assertTrue(len(cl3.certain) > 1)
        # and work
        self.assertEqual(h3, hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new(cl3.certain[0])))

    
    def test_multi(self):
        # test all hashing functions
        algo = "md5"

        h1 = hashit.hashFile(FILE, hashit.new(algo), True)
        h2 = hashit.hashFile(FILE, hashit.new(algo))
        h3 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new(algo))

        # just checking
        self.assertEqual(hashit.detect(hashit.hashFile(FILE, hashlib.sha224(), False), hashit.generate_data_set("HALLO", hashit.__algorithems__, hashit.new)).certain[0], "sha224")

        self.assertTrue(h1 == h2 == h3 == FILE_SUM)
    

    def test_systemrandom(self):
        # test system random
        generate = lambda k=2: ''.join([random.SystemRandom().choice(string.hexdigits) for i in range(k)])

        all_gen = list()
        c_str = generate()

        while not c_str in all_gen:
            all_gen.append(c_str)
            c_str = generate()

        print(c_str, "in list (COLLISION FOUND) after", len(all_gen), "Tries, which translates into", unhexlify(c_str))
        self.assertTrue(c_str in all_gen)
        
    def test_crc32(self):
        crc = lambda d=b'': hashit.new("crc32", d).hexdigest()
        done = {}

        for n in range(100000000):
            n = str(n)
            h = crc(n.encode())
            if h in done.keys():
                print("ERROR collision found in CRC32", h, n, "and", done[h])
                break

            done[h] = n


    def test_other(self):
        self.assertIsInstance(hashit.supports_color(), bool)
        
        with self.assertRaises(SystemExit):
            hashit.__main__.main(["--help"])
        
        with self.assertRaises(SystemExit):
            hashit.__main__.main(["--check", "file_name"])

        # just checking
        self.assertEqual(hashit.__author__, "Javad Shafique")
        # check the sfv parser
        self.assertEqual(hashit.sfv_max("abc", "def", 4), "def  abc")



if __name__ == "__main__":
    unittest.main()
