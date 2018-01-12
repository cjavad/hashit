import unittest, hashlib, sys, subprocess
sys.path.insert(0, "..")
import hashit
import hashit.__main__

class Test(unittest.TestCase):
    def test_hasher(self):
        # use md5sum to compare with
        md5sum_of_self = subprocess.check_output(['md5sum', 'unit.py']).decode().split(" ")[0]
        h = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.md5())
        self.assertEqual(h, md5sum_of_self)

    def test_detect(self):
        # generate data set
        ds = hashit.generate_data_set("Hallo", hashit.__algorithems__, hashlib.new)

        # hash file three times
        h1 = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.md5())
        h2 = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.sha224())
        h3 = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.sha1())

        # detect for three algorigthms
        cl1 = hashit.detect(h1, ds)
        cl2 = hashit.detect(h2, ds)
        cl3 = hashit.detect(h3, ds)

        # correct hash names
        correct1 = "md5"
        correct2 = "sha224"

        # md5 or md4
        self.assertTrue(correct1 in cl1.maybe)

        # only one left should be true
        self.assertTrue(correct2 in cl2.certain)
        # and if it is to check hash with it
        self.assertEqual(hashlib.new(correct2, b'Hallo').hexdigest(), hashlib.new(cl2.certain[0], b'Hallo').hexdigest())

        # for sha1 more options should be avaible
        self.assertTrue(len(cl3.certain) > 1)
        # and work
        self.assertEqual(h3, hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.new(cl3.certain[0])))

    def test_multi(self):
        # test all hashing functions
        algo = "md5"

        md5sum_of_self = subprocess.check_output(['md5sum', 'unit.py']).decode().split(" ")[0]
        h1 = hashit.easy_hash("unit.py", hashlib.new(algo))
        h2 = hashit.hashFile("unit.py", hashlib.new(algo))
        h3 = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.new(algo))

        # just checking
        self.assertEqual(hashit.detect(hashit.hashFile("unit.py", hashlib.sha224(), False), hashit.generate_data_set("HALLO", hashit.__algorithems__, hashlib.new)).certain[0], "sha224")

        self.assertTrue(h1 == h2 == h3 == md5sum_of_self)

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
