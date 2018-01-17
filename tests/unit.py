from __future__ import print_function
import unittest, hashlib, sys, subprocess, random, string
from binascii import unhexlify # python3 support
sys.path.insert(0, "..")
import hashit
import hashit.__main__

# NOTE THE TESTS REQUIRE A MD5-CHECKSUM of a file as a point of comparionsing

FILE = "LICENSE"
FILE_SUM = "8ca87f6e5e1480c2a83cc0f76fb1276b"

# check sums for file
FILE_SUMS = {
    "DSA": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "DSA-SHA": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "blake2b": "27c1dad8331065b4eec0c5767631fe2e1e3d8d327cfbd9d406618eef98b88399dc9aa410ab8d1dec1021671083a72572fbc054e210532563ff5c2235fc2ec794",
    "blake2s": "5bd9d53a9e8caf717ee4028968df3beda69320c981b503b2bf905090a7734244",
    "crc32": "43be10fe",
    "dsaEncryption": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "dsaWithSHA": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "ecdsa-with-SHA1": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "md4": "34bcfe03311b48576b259fd1f8df3743",
    "md5": "8ca87f6e5e1480c2a83cc0f76fb1276b",
    "ripemd160": "635d845687ce3f548ce328384f456a66f5f5b992",
    "sha": "b3a66501bcf4273e281e6469ba0d50e4aca7dc8a",
    "sha1": "3dba84c57f97eade3e754a6739e0d1b13bf3ea35",
    "sha224": "6479610a2cd48f07748e198a9ae343fa2ffbee2ea31bec8c88887f97",
    "sha256": "e7434be58d1f9c3d37c33b4f0b627ffc94a1bdc5cdd06cd3a8d40db0aec6aec2",
    "sha384": "dde49e5e7615138a38fd1e7955bacc04d1921706b445889115165df50215fa3c37bbee8089a4b70315475b8f8e05db67",
    "sha512": "05c7499712855e34cbbaf5a6e381a28e9749980d1e43787bb5fc8d5dbf666d4d6eb06705ee9503c84cf0a86a0ab04b27441ea74bdb69dfdc0484ada489ecb519",
    "whirlpool": "327cfa505f50abe31cfd4914e7b86005174fb04c8909cffe005ed663a02afbd7b5ddc4154d79e8cd529a06bcad974d2be130fbdef0037abe44d48855d3f0f40c"
}

class Test(unittest.TestCase):
    def test_hasher(self):
        for algo in hashit.__algorithems__:
            h1 = hashit.new(algo, open(FILE, "rb").read()).hexdigest()
            h2 = hashit.hashFile(FILE, hashit.new(algo), True)
            self.assertEqual(h1, h2)
            self.assertEqual(h1, FILE_SUMS[algo])

        h1 = hashit.new("md5", open(FILE, "rb").read()).hexdigest()
        self.assertEqual(h1, FILE_SUM)


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
