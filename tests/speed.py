import timeit, os, json
os.sys.path.insert(0, "..")
import hashit

def hashfile(file, algo):
    return hashit.hashIter(hashit.blockIter(open(file, "rb")), hashit.hashlib.new(algo))

def hashstr(string, algo):
    return hashit.hashlib.new(algo, string.encode()).hexdigest()

    return 

def gen(n=timeit.default_number):
    for algo in hashit.__algorithems__:
        x = timeit.timeit("hashfile('speed.py', '" + algo + "')", setup="from __main__ import hashfile", number=n)
        x2 = timeit.timeit("hashstr('"+ str(x) + "', '" + algo + "')", setup="from __main__ import hashstr", number=n)
        yield {"algo":algo, "file-time":x,"str-time":x2,"number":n} 

o = dict()
for i in gen():
    o.update({i["algo"]:i})

open("OUT.json", "w").write(json.dumps(o, indent=4, sort_keys=True))
