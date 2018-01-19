"""Benchmarking for hashits hashing functions and algorithms"""
from __future__ import print_function
import timeit, os, json, hashlib
from memory_profiler import profile
os.sys.path.insert(0, "..")
import hashit


# do not use, at least 10 times slower than any other method
def easy_hash(filename, hasher):
    """Slow but easy to use self-contained hasher"""
    filename = filename
    # openfile
    with open(filename, "rb") as afile: 
        for block in (line for line in afile.readlines()):
            hasher.update(block)
    # return hash
    return hasher.hexdigest()

if os.sys.version_info[0] == 2:
    global input
    input = raw_input

# takes algorithem
def hashfile(file, algo):
    return hashit.hashIter(hashit.blockIter(open(file, "rb")), hashit.new(algo))

def hashstr(string, algo):
    return hashit.new(algo, string.encode()).hexdigest() 


def slow_hashfile(file, algo):
    return hashit.new(algo, open(file, "rb").read()).hexdigest()


def easy_hashfile(file, algo):
    return easy_hash(file, hashit.new(algo))



def gen(n=timeit.default_number):
    for algo in hashit.__algorithems__:
        x = timeit.timeit("hashfile('speed.py', '" + algo + "')", setup="from __main__ import hashfile", number=n)
        x2 = timeit.timeit("hashstr('"+ str(x) + "', '" + algo + "')", setup="from __main__ import hashstr", number=n)
        yield {"algo":algo, "file-time":x,"str-time":x2,"number":n} 


def test1(n=timeit.default_number, filename=None):
    o = dict()
    for i in gen(n):
        o.update({i["algo"]:i})

    open((filename or input("Output to: ")), "w").write(json.dumps(o, indent=4, sort_keys=True))


def parse_test1(jsonfile):
    data = json.loads(open(jsonfile, "r").read())

    def findt(s):
        sorted_list = sorted(data, key=lambda key: data[key][s])
        for c, i in enumerate(sorted_list):
            sorted_list[c] = i + ": " + str(data[i][s])
        
        return sorted_list

    print("Fastest to slowest file\n   ", '\n    '.join(findt("file-time")), end='\n\n')
    print("Fastest to slowest string\n   ", '\n    '.join(findt("str-time")), end='\n\n')



# where default big file is an 512M file
#@profile
def test2(algo, n=1000, bigfile="/home/javad/filename"):
    if algo in hashit.__algorithems__:
        fast = timeit.timeit("hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import hashfile", number=n)
        print("Fast:", fast)
        all_in = timeit.timeit("slow_hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import slow_hashfile", number=n)
        print("All in:", all_in)
        easy = timeit.timeit("easy_hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import easy_hashfile", number=n)
        print("Easy:", easy)
'''
10000:
 Fast: 5.277344635996997
 All in: 3.604332027996861
 Easy: 35.06488174900005
 Filename: speed.py

1000000:
 Fast: 54.695157744000085
 All in: 40.071381821000045
 Easy: 880.830499345
 Filename: dataset_from_detect.json

'''

#test2("md5", 1000000, path_to_large_file)

if __name__ == "__main__":
    # hash with a bunch of algorigthms a million times each and compare results
    if not (os.path.exists("./res/benchmarks.json") and os.path.exists("./res/benchmarks2.json")):
        test1(100000, "./res/benchmarks.json")
        test1(100000, "./res/benchmarks2.json")

    parse_test1("./res/benchmarks.json")
    parse_test1("./res/benchmarks2.json")

    test2("sha256", bigfile="./res/file.json")