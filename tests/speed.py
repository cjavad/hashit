import timeit, os, json
from memory_profiler import profile
os.sys.path.insert(0, "..")
import hashit


def hashfile(file, algo):
    return hashit.hashIter(hashit.blockIter(open(file, "rb")), hashit.hashlib.new(algo))

def hashstr(string, algo):
    return hashit.hashlib.new(algo, string.encode()).hexdigest() 


def slow_hashfile(file, algo):
    return hashit.hashlib.new(algo, open(file, "rb").read()).hexdigest()


def easy_hashfile(file, algo):
    return hashit.easy_hash(file, hashit.hashlib.new(algo))

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
        sorted_list = sorted(data.keys(), key=lambda key: data[key][s])
        for c, i in enumerate(sorted_list):
            sorted_list[c] = i + ": " + str(data[i][s])
        
        return sorted_list

    print("Fastest to slowest file\n   ", '\n    '.join(findt("file-time")), end='\n\n')
    print("Fastest to slowest string\n   ", '\n    '.join(findt("str-time")), end='\n\n')



# where big file is an 512M file
@profile
def test2(algo, n=1000, bigfile="/home/javad/filename"):
    if algo in hashit.__algorithems__:
        fast = timeit.timeit("hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import hashfile", number=n)
        print("Fast:", fast)
        slow = timeit.timeit("slow_hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import slow_hashfile", number=n)
        print("Slow:", slow)
        easy = timeit.timeit("easy_hashfile('" + bigfile + "', '"+algo+"')", setup="from __main__ import easy_hashfile", number=n)
        print("Easy:", easy)
'''
Fast: 5.277344635996997
Slow: 3.604332027996861
Easy: 35.06488174900005
''' 
#test2("md5", 100000, "unit.py")

# hash with a bunch of algorigthms a million times each and compare results
#test1(1000000, "benchmarks.json")
#test1(1000000, "benchmarks2.json")

parse_test1("benchmarks.json")
parse_test1("benchmarks2.json")