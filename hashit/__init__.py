# import print and with for python2 support
from __future__ import print_function, with_statement
from .version import __version__ # global version
import hashlib, os 



__author__ = "Javad Shafique" # copyrigth holder
__license__ = "MIT, Copyrigth (c) 2017-present Javad Shafique" # license foro program

# help message
# this list is the message that will be printed
# when the user uses hashit --help

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

# hash_bytestr_iter goes over an bytes string
# block for block and updates the hash while
# not having the intire file in memory

def hash_bytestr_iter(bytesiter, hashit, ashexstr=True):
    for block in bytesiter:
        hashit.update(block)
    return (hashit.hexdigest() if ashexstr else hashit.digest())

# file_as_blockiter creates bytestring-blocked
# byte data for hash_bytestr_iter

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

# check reads an file generate with hashit > outfile
# and compares the results by re-hashing the file
# and print if there is a change

def check(path, hashit):
    x = open(path, "r").readlines()
    for i in x:
        m = i.split(" ")
        
        # Wrong format
        if len(m) != 2:
            continue
        
        # get hash and file path
        hashis = m[0].replace("\n", "").replace("\0", "")
        fname = m[1].replace("\n", "").replace("\0", "")


        try:
            # try to hash it again
            chash = str(hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashit))
        except:
            print("Error while reading", fname)
            continue # ehmm file does seem not exist

        if chash != hashis:
            # if the file has changed print notice
            print(fname, "is changed from", hashis, "to", chash)

def main(args = None):
    # Varibles
    FILES = list() # list of all files
    M_path = os.getcwd() # path to search in

    # switch args if needed
    if args == None:
        # to sys.args
        args = os.sys.argv[1:]
    
    # Switch-index where the last argument is
    SW_index = int()

    # first switch
    if len(args) >= 1:
        # if you want to check
        if args[0] == "check" and len(args) >= 2:
            # select hash
            hashit = hashlib.md5()
            if len(args) >= 3:
                # md5
                if args[2].lower() == "md5":
                    hashit = hashlib.md5()
                # sha256
                elif args[2].lower() in ("sha256", "sha_256", "sha-256"):
                    hashit = hashlib.sha256()
                # sha1 (Do not use)
                elif args[2].lower() in ("sha1", "sha_1", "sha-1"):
                    hashit = hashlib.sha1()
            # and check
            check(args[1], hashit)
            exit()
        # select path
        if args[0].count("/") > 0 or args[0].count("\\") > 0:
            M_path = args[0]
            SW_index = 1

        # quick-select path thing
        elif args[0] == ".":
            M_path = "./"
        # parent dir
        elif args[0] == "..":
            M_path = "../"

        # else reset SW_index
        else:
            SW_index = 0
        
    # walk directory
    for path, subdirs, files in os.walk(M_path):
        # for each file
        for name in files:
            # add it to FILES list() 
            FILES.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))
    # select hash
    hasha = hashlib.md5()

    # use SW_index to get its' index in the argument list
    if len(args) >= SW_index + 1:
        # md5
        if args[SW_index].lower() == "md5":
            hasha = hashlib.md5()
        # sha256
        elif args[SW_index].lower() in ("sha256", "sha_256", "sha-256"):
            hasha = hashlib.sha256()
        # sha1 (Do not use)
        elif args[SW_index].lower() in ("sha1", "sha_1", "sha-1"):
            print("DECPRECATED! Do not use sha1")
            hasha = hashlib.sha1() # DECPRECATED

        # Check for commands
        # --help print help
        elif args[SW_index] == "--help":
            for i in HELP:
                print(i)
            exit()
        # print version
        elif args[SW_index] == "--version":
            print(__version__)
            exit()
        # print author
        elif args[SW_index] == "--author":
            print(__author__)
            exit()
        # print license
        elif args[SW_index] == "--license":
            print(__license__)
            exit()
        
        # else set hash to md5 (just to make sure)
        else:
            hasha = hashlib.md5()
    # simplefy path
    M_path = M_path.replace("\\", "/")

    # go over files and hash them all
    for fname in FILES:
        try:
            i = str(hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hasha)) + " " + str(fname)
        except:
            # skip
            continue
        
        # if the last arguemnt is true then remove fullpath
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

# main
if __name__ == "__main__":  
    main()
