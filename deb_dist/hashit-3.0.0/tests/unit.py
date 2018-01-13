from __future__ import print_function
import unittest, hashlib, sys, subprocess, random, string
from binascii import unhexlify # python3 support
sys.path.insert(0, "..")
import hashit
import hashit.__main__

# NOTE THE TESTS REQUIRE A MD5-CHECKSUM of a file as a point of comparionsing

FILE = "LICENSE"
FILE_SUM = "c9ca86e6b436c4cc98d62d336f0b5369"

# check sums for file
FILE_SUMS = {
    "md4":"324c4e0b6529f5185ee2afaff06397ba",
    "md5":"c9ca86e6b436c4cc98d62d336f0b5369",
    "sha1":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "DSA":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "ecdsa-with-SHA1":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "dsaEncryption":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "DSA-SHA":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "dsaWithSHA":"529c3dca5681db4e2b37a7909064dfe2344ec095",
    "sha":"558a4c1c3f0afbe6280f10a5370649db495d5011",
    "sha224":"0991203002e4412141f21808bec216b65c17c1ecc5b6d299f53c8b5d",
    "sha256":"785e3de164e5c7787e9bb856707fe8d565e1d76823939eff226ca1c6666cac18",
    "sha384":"acfc0018b0ed7ced42d3e83c14fc85d009a4541612063b4660e0b09b4651a728cc21d477284eaa845528effad68bb9be",
    "sha512":"89f83d0ae1ca66c386c0c271e440b37967e3ab495b36a20a8ca67445135febef461baa92a67870c81f998509212f5da308f816e4c95b8c0ea2625488be341bb0",
    "ripemd160":"ae16a3dfbb4aed2e2a2564ab4f24bdc090de925a",
    "whirlpool":"b6c954e249f9dac08aeba5a72742471f48a98b7d0f98dc075fc68884ed9df7bf0ddfb4b9922b269a554524d9e3a110dca5fd7a2d452891ece092ed5028efb1fa",
    "crc32":"5cb92e3e",
    "blake2s":"f6e4ed248c729474ba235b08e7415facf586f99aadf23b8ba2ff186ef7dcf26c",
    "blake2b":"2dc623f7f3f81b2b7cdb5ae496a72ef93f20147f5a653a4d61374384cc42f3ef14ae67403e2b3152da6e842d76b24061cb3510cdbc9f403ae900d9dc9d536a2e"
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
