from __future__ import print_function, with_statement
import unittest
import os, sys
import random, string
from .test_load import load_api_1, load_api_2, load_api_3
from .config import FILE, FILE_SUM, FILE_SUMS
from binascii import unhexlify # python3 support
sys.path.insert(0, "..")
import hashit
import hashit.__main__

if not os.path.exists(FILE):
    os.chdir("..")

# use with for this, to disable stdout and stderr
class DisablePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close os.devnull
        sys.stderr.close()
        sys.stdout.close()
        # set default
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

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
        h1 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new("md5"))
        h2 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new("sha224"))
        h3 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new("sha1"))
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
        self.assertTrue(correct2 in (cl2.certain if cl2.certain else cl2.maybe))
        self.assertTrue(correct4 in cl4.certain)
        # and if it is to check hash with it
        self.assertEqual(hashit.new(correct2, b'Hallo').hexdigest(), hashit.new(cl2.certain[0] if cl2.certain else cl2.maybe[0], b'Hallo').hexdigest())

        # for sha1 more options should be avaible
        self.assertTrue(len(cl3.certain) > 1)
        # and work
        self.assertEqual(h3, hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new(cl3.maybe[0])))

    def test_detect_format(self):
        # create shortcut
        df = lambda s: hashit.detect_format(s)
        
        bsdstr = hashit.BSD.format("12345678", "/path/to/file.txt", "crc32")
        sfvstr = hashit.SFV.format("12345678", "/path/to/file.txt", 18, "")
        nonata = "{} {}".format("12345678", "/path/to/file.txt")

        self.assertEqual(df(bsdstr), "bsd")
        self.assertEqual(df(sfvstr), "sfv")
        self.assertEqual(df(nonata), "N/A")
    
    def test_multi(self):
        # test all hashing functions
        algo = "md5"

        h1 = hashit.hashFile(FILE, hashit.new(algo), True)
        h2 = hashit.hashFile(FILE, hashit.new(algo))
        h3 = hashit.hashIter(hashit.blockIter(open(FILE, "rb")), hashit.new(algo))

        # just checking
        d = hashit.detect(hashit.hashFile(FILE, hashit.new("sha224"), False), hashit.generate_data_set("HALLO", hashit.__algorithms__, hashit.new))
        self.assertEqual(d.certain[0] if d.certain else d.maybe[0], "sha224")

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
        
        with DisablePrint():
            with self.assertRaises(SystemExit):
                hashit.__main__.main(["--help"])
            
            with self.assertRaises(SystemExit):
                hashit.__main__.main(["--check", "file_name"])
            

        # just checking
        self.assertEqual(hashit.__author__, "Javad Shafique")

class TestLoad(unittest.TestCase):
    def test_load(self):
        hashit.load(load_api_1)
        h1 = hashit.new("hash1", b'data')
        self.assertEqual(hex(h1.digest()), h1.hexdigest())

    def test_load_all(self):
        hashit.load_all([load_api_2, load_api_3])
        h2 = hashit.new("hash2", b'data')
        h3 = hashit.new("hash3", b'data')
        self.assertEqual(hex(h2.digest()), h2.hexdigest())
        self.assertEqual(hex(h3.digest()), h3.hexdigest())