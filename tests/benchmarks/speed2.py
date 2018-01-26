"""Speed tests comparing pycrypto and hashlib's hash functions in terms of performance"""
from __future__ import print_function
import timeit, os, json, hashlib
from Crypto.Hash import MD4, MD5, SHA224, SHA256, SHA384, SHA512, SHA, RIPEMD
os.sys.path.insert(0, "..")
import hashit


if os.sys.version_info[0] == 2:
    global input
    input = raw_input

# dict with hashers
hashers = {
        "md4":{"hashlib_hash":hashlib.new("md4"), "crypto_hash":MD4.MD4Hash()},
        "md5":{"hashlib_hash":hashlib.new("md5"), "crypto_hash":MD5.MD5Hash()},
        "sha224":{"hashlib_hash":hashlib.new("sha224"), "crypto_hash":SHA224.SHA224Hash()},
        "sha256":{"hashlib_hash":hashlib.new("sha256"), "crypto_hash":SHA256.SHA256Hash()},
        "sha384":{"hashlib_hash":hashlib.new("sha384"), "crypto_hash":SHA384.SHA384Hash()},
        "sha512":{"hashlib_hash":hashlib.new("sha512"), "crypto_hash":SHA512.SHA512Hash()},
        "sha1":{"hashlib_hash":hashlib.new("sha1"), "crypto_hash":SHA.SHA1Hash()},
        "ripemd160":{"hashlib_hash":hashlib.new("ripemd160"), "crypto_hash":RIPEMD.RIPEMD160Hash()}
        }

# takes hasher
def hashFile(filename, hasher):
    return hashit.hashIter(hashit.blockIter(open(filename, "rb")), hasher)
    
def hashStr(binary, hasher):
    hasher.update(binary)
    return hasher.hexdigest()

def NoMemFile(filename, hasher):
    hasher.update(open(filename, "rb").read())
    return hasher.hexdigest()

def RawCompare(algo, file="speed2.py", n=100000):
    # create command
    cC = lambda key, filename, command, algorihtm=algo: "{}('{}', hashers['{}']['{}'])".format(command, filename, algorihtm, key)
    setup = "from __main__ import hashFile, NoMemFile, hashers"

    Mem_H, Mem_C = timeit.timeit(cC("hashlib_hash", file, "hashFile"), setup=setup, number=n), \
        timeit.timeit(cC("crypto_hash", file, "hashFile"), setup=setup, number=n)

    NoMem_H, NoMem_C = timeit.timeit(cC("hashlib_hash", file, "NoMemFile"), setup=setup, number=n), \
        timeit.timeit(cC("crypto_hash", file, "NoMemFile"), setup=setup, number=n)

    print(Mem_H, NoMem_H)
    print(Mem_C, NoMem_C)

# generate dataset for CompareCnH
def CryptoVsHashlib(file_to_hash="speed.py", data_to_hash="Hello World!", n=timeit.default_number):
    # dict for results
    results = {
        "md4":{},
        "md5":{},
        "sha224":{},
        "sha256":{},
        "sha384":{},
        "sha512":{},
        "sha1":{},
        "ripemd160":{}
    }
    for algo in hashers:
        # hashlib_hash for hashlib and crypto_hash for crypto (pycrypto(dome))
        # first hash an file
        h_file = timeit.timeit("hashFile('{}', hashers['{}']['hashlib_hash'])".format(file_to_hash, algo), setup="from __main__ import hashFile, hashers", number=n)
        c_file = timeit.timeit("hashFile('{}', hashers['{}']['crypto_hash'])".format(file_to_hash, algo), setup="from __main__ import hashFile, hashers", number=n)

        h_str = timeit.timeit("hashStr(b'{}', hashers['{}']['hashlib_hash'])".format(data_to_hash, algo), setup="from __main__ import hashStr, hashers", number=n)
        c_str = timeit.timeit("hashStr(b'{}', hashers['{}']['crypto_hash'])".format(data_to_hash, algo), setup="from __main__ import hashStr, hashers", number=n)

        results[algo]["hashlib_hash"] = {"file":h_file, "str":h_str}
        results[algo]["crypto_hash"] = {"file":c_file, "str":c_str}

    return results

# use CryptoVsHashlib to compare speed

def CompareCnH(output=None, amount_of_datasets=100, n=1000):
    res = list()
    for _ in range(amount_of_datasets):
        res.append(CryptoVsHashlib(n=n))

    res2 = dict()

    for algo in hashers:
        res2[algo] = {}
        res2[algo]["crypto_hash"] = {"file":0, "str":0, "amount-file":[], "amount-str":[]}
        res2[algo]["hashlib_hash"] = {"file":0, "str":0, "amount-file":[], "amount-str":[]}

        other = lambda x: "crypto_hash" if x == "hashlib_hash" else "hashlib_hash" # switch to the opposite

        for ds in res:
            ff = max(ds[algo], key=lambda key: ds[algo][key]["file"])
            fs = max(ds[algo], key=lambda key: ds[algo][key]["str"])
            res2[algo][ff]["file"] += 1
            res2[algo][ff]["amount-file"].append(ds[algo][ff]["file"] - ds[algo][other(ff)]["file"])
            res2[algo][fs]["str"] += 1
            res2[algo][fs]["amount-str"].append(ds[algo][fs]["str"] - ds[algo][other(fs)]["str"])

    # write output to file
    open((output or str(input("Output to: "))), "w").write(json.dumps({"datasets":res, "results":res2}, indent=4, sort_keys=True))

def ReadCnH(filename):
    res2 = json.loads(open(filename, "r").read())["results"]
    # print data
    for algo in hashers:
        f_file = max(res2[algo], key=lambda key: res2[algo][key]["file"])
        f_str = max(res2[algo], key=lambda key: res2[algo][key]["str"])

        print("Fastest", algo, "For files", f_file, )
        print("Fastest", algo, "For strings", f_str)

if __name__ == "__main__":
    
    if not os.path.exists("./res/pycrypto_vs_hashlib.json"):
        CompareCnH(output="./res/pycrypto_vs_hashlib.json")

    ReadCnH("./res/pycrypto_vs_hashlib.json")