import unittest, hashlib, sys, subprocess
sys.path.insert(0, "..")
import hashit

class Test(unittest.TestCase):
    def test_hasher(self):
        # use md5sum to compare with
        md5sum_of_self = subprocess.check_output(['md5sum', 'unit.py']).decode().split(" ")[0]
        h = hashit.hashIter(hashit.blockIter(open("unit.py", "rb")), hashlib.md5())
        self.assertEqual(h, md5sum_of_self)
        self.hashis = h

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

    def test_other(self):
        self.assertTrue(type(hashit.supports_color()) == bool)

if __name__ == "__main__":
    unittest.main()