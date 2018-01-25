from __future__ import print_function
import unittest, hashlib, os, random, string
from binascii import unhexlify # python3 support
os.sys.path.insert(0, "..")
import hashit
import hashit.__main__

# NOTE THE TESTS REQUIRE A MD5-CHECKSUM and a CHECKSUM-table of a file as a point of comparionsing

FILE = "LICENSE"
FILE_SUM = "c11869fc956d819d2a336c74f4cc6000"

if not os.path.exists(FILE):
    os.chdir("..")

# check sums for file
FILE_SUMS = {
    "DSA": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "DSA-SHA": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "blake2b": "a64b7235b81d307b919c0d74ded6c86b823e2b9b2a9c1e50e55e273daedd5417027f2a2a1b4abc5d72be5170b462979867cae4b8c3fcf8a7d8a09a1c93fc9d11",
    "blake2s": "1ecfc726c59ec5cd52a24730e3345a650d4a2554b1b1dc50ed9c1faf9ebd8179",
    "crc32": "3371bb00",
    "dsaEncryption": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "dsaWithSHA": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "ecdsa-with-SHA1": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "md4": "1901cf76521dfb68b0a88df72c995345",
    "md5": "c11869fc956d819d2a336c74f4cc6000",
    "ripemd160": "7fbabc556593e015495d752a0f8ba1d99eee0f8a",
    "sha": "597018a568e01f2434ce967be416beaefff02536",
    "sha1": "05d9842ff5ab98ea012b1cbe2693a0714a33547a",
    "sha224": "16ac30faa8d42524bc70f3f52412680ada5993d401ca057edfe3cdec",
    "sha256": "81be97a4c17e703ddce3cfe0bd774aba4d67d4e3f225da4b4071a75388132aca",
    "sha384": "b4efcc718ecf169bddbaeb023694071193a255d57674144220f9880544da1feaee0a218043ae00cbd3fbe2e84900e771",
    "sha512": "70ef754d5a3f87b7a545bce7360f20327b17f094fc75f3fc095551d6ea9e2459b1bbc7d22f26971d7716a8d204e83b33b169099544bc7c32feac26a31090cc39",
    "whirlpool": "f6f74448a5ea9553387678f68146d0f38dd639e644e547840077cd39a6c20a23452d28d8758aa2aba03bcb2eba38b350050ec5fecc52d1f813ae0e1892994ce8"
}

class Test(unittest.TestCase):
    def test_hasher(self):
        file = open(FILE, "rb")
        data = file.read()

        for algo in hashit.__algorithms__:
            h1 = hashit.new(algo, data).hexdigest()
            h2 = hashit.hashFile(FILE, hashit.new(algo), True)
            self.assertEqual(h1, h2)
            self.assertEqual(h1, FILE_SUMS[algo])

        h1 = hashit.new("md5", data).hexdigest()
        self.assertEqual(h1, FILE_SUM)
        file.close()

    def test_detect(self):
        # generate data set
        ds = hashit.generate_data_set("Hallo", hashit.__algorithms__, hashit.new)

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
        self.assertEqual(hashit.detect(hashit.hashFile(FILE, hashlib.sha224(), False), hashit.generate_data_set("HALLO", hashit.__algorithms__, hashit.new)).certain[0], "sha224")

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
        """
        crc = lambda d=b'': hashit.new("crc32", d).hexdigest()
        done = {}

        for n in range(100000000):
            n = str(n)
            h = crc(n.encode())
            if h in done:
                print("ERROR collision found in CRC32", h, n, "and", done[h])
                break
            try:
                done[h] = n
            except MemoryError:
                done.clear()
        """

    def test_format(self):
        s = hashit.BSD.format(FILE_SUM, FILE, "md5")
        self.assertEqual(s, "md5 ({}) = {}".format(FILE, FILE_SUM))
        self.assertEqual(hashit.BSD.parser(s), ["md5", FILE, FILE_SUM])

        # check the sfv parser
        self.assertEqual(hashit.SFV.format("abc", "def", 4), "def  abc")



    def test_other(self):
        self.assertIsInstance(hashit.supports_color(), bool)
        
        with self.assertRaises(SystemExit):
            hashit.__main__.main(["--help"])
        
        with self.assertRaises(SystemExit):
            hashit.__main__.main(["--check", "file_name"])

        # just checking
        self.assertEqual(hashit.__author__, "Javad Shafique")



if __name__ == "__main__":
    unittest.main()
