from __future__ import print_function, with_statement
from .version import __version__ # version
import hashlib, os



__author__ = "Javad Shafique"
__license__ = "MIT, Copyrigth (c) 2017-present Javad Shafique"

HELP = [
    "",
    "Usage:",
    "   hashit $path $hash (md5, sha256, sha1)",
    "Or:",
    "   hashit $hash (md5, sha256, sha1)",
    "Or just:",
    "   hashit (uses current dir and md5 hashing)",
    "",
    "and the if the last argument is 'True' then the full path will be removed",
    "but then you can only run check in the same path",
    "",
    "For checking use this scheme:",
    "   hashit 'check' $pathtooutput $hash (optional, uses md5 by defuault)",
    ""
]


def hash_bytestr_iter(bytesiter, hashit, ashexstr=True):
    for block in bytesiter:
        hashit.update(block)
    return (hashit.hexdigest() if ashexstr else hashit.digest())

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def check(path, hashit):
    x = open(path, "r").readlines()
    for i in x:
        m = i.split(" ")
        
        # Wrong format
        if len(m) != 2:
            continue

        hashis = m[0].replace("\n", "").replace("\0", "")
        fname = m[1].replace("\n", "").replace("\0", "")
        chash = str(hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashit))

        if chash != hashis:
            print(fname, "is changed from", hashis, "to", chash)

def main(args = None):
    FILES = list()
    OUT = list()
    M_path = os.getcwd()

    if args == None:
        args = os.sys.argv[1:]
    
    SW_index = int()

    if len(args) >= 1:
        if args[0] == "check" and len(args) >= 2:
            hashit = hashlib.md5()
            if len(args) >= 3:
                if args[2].lower() == "md5":
                    hashit = hashlib.md5()
                elif args[2].lower() in ("sha256", "sha_256", "sha-256"):
                    hashit = hashlib.sha256()
                elif args[2].lower() in ("sha1", "sha_1", "sha-1"):
                    hashit = hashlib.sha1()

            check(args[1], hashit)
            exit()

        if args[0].count("/") > 0 or args[0].count("\\") > 0:
            M_path = args[0]
            SW_index = 1
        elif args[0] == ".":
            M_path = "./"
        elif args[0] == "..":
            M_path = "../"
        else:
            SW_index = 0
        

    for path, subdirs, files in os.walk(M_path):
        for name in files: 
            FILES.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))

    hasha = hashlib.md5()

    if len(args) >= SW_index + 1:
        if args[SW_index].lower() == "md5":
            hasha = hashlib.md5()

        elif args[SW_index].lower() in ("sha256", "sha_256", "sha-256"):
            hasha = hashlib.sha256()

        elif args[SW_index].lower() in ("sha1", "sha_1", "sha-1"):
            print("DECPRECATED! Do not use sha1")
            hasha = hashlib.sha1() # DECPRECATED

        elif args[SW_index] == "--help":
            for i in HELP:
                print(i)
            exit()

        elif args[SW_index] == "--version":
            print(__version__)
            exit()

        elif args[SW_index] == "--author":
            print(__author__)
            exit()

        elif args[SW_index] == "--license":
            print(__license__)
            exit()
            
        else:
            hasha = hashlib.md5()

    M_path = M_path.replace("\\", "/")

    for fname in FILES:
        try:
            i = str(hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hasha)) + " " + str(fname)
        except:
            # skip
            continue
        

        if len(args) >= 1:
            if args[len(args) - 1] == "True":
                print(i.replace(M_path, "."))
            else:
                # if there if more than one argument
                print(i)
                pass
        else:
            print(i)
            pass

if __name__ == "__main__":  
    main()
