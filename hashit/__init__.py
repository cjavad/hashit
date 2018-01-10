# import print and with for python2 support
from __future__ import print_function, with_statement
from .version import __version__ # global version
from argc import argc
import hashlib, os 


__author__ = "Javad Shafique" # copyrigth holder
__license__ = "MIT, Copyrigth (c) 2017-present Javad Shafique" # license foro program

# help message
# this list is the message that will be printed
# when the user uses hashit --help

# fix algo list
__algorithems__ = [s for s in hashlib.algorithms_available if not (str(s)[:5] in ("sha3_", "shake") or str(s)[:3] in ("SHA", "MD5", "MD4") or str(s) in ("RIPEMD160"))]

__help__ = [
    "Usage:\n",
    "   hashit $args",
    "",
    "Arguments:\n",
    "   -v --version: prints current version",
    "   -h --help: prints this message",
    "   -l --license: prints license",
    "   -p --path $path: sets path default $current",
    "   -H --hash $type: sets hash in this list \n\n      {}\n".format('\n      '.join(__algorithems__)),
    "   -c --check $filepath: reads output from this program and checks for change",
    "   -o --output $filepath: writes output to file same as '>' operator",
    "   -C --color: enables colored output. Only for check (-c, --check)"
    "   ",
    "   Use 'True' at the end for only outputting the releative path not the fullpath",
    "",
    "Notice: this program was made by Javad Shafique, and uses argc another package by me"
]

# check if terminal supports color from django
def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = os.sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(os.sys.stdout, 'isatty') and os.sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

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

def check(path, hashit, color = False):
    RED = b"\x1b[0;31m".decode("ascii")
    GREEN = b"\x1b[0;32m".decode("ascii")
    RESET = b"\x1b[0m".decode("ascii")

    # check if system supports color
    # with bitwise-exclusive or (XOR)
    if supports_color() ^ color:
        RED = ""
        GREEN = ""
        RESET = ""
    
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
            # if the file has changed print notice (md5 sum inpired)
            print(fname + ":" + GREEN, hashis + RESET, ">", RED + chash, end=RESET + '\n')
        else:
            print(fname + ":" + GREEN, "OK", end=RESET + '\n')

def main(args = None):
    # switch args if needed
    if args == None:
        # to sys.args
        args = os.sys.argv[1:]
    
    # using argc module by me (support for python2)
    argv = argc(args, False)
    # set commands
    argv.set("-h", "--help", "help", "Print help message", None, __help__, True)
    argv.set("-v", "--version", "version", "Print version", None, __version__, True)
    argv.set("-l", "--license", "license", "Prints licenses", None, __license__, True)
    # set arguments
    argv.set("-H", "--hash", "hash", "Select hash", None)
    argv.set("-p", "--path", "path", "Path to scan", None)
    argv.set("-c", "--check", "check", "Check files", None)
    argv.set("-o", "--output", "output", "Output file", None)
    argv.set("-C", "--color", "color", "Set color true/false", False)

    # run (can raise SystemExit)
    argv.run()
    # Varibles
    FILES = list() # list of all files
    M_path = os.getcwd() # path to search in

    # get hash from arguments
    # default is md5 for now
    # it supports md5 and sha256
    hashIs = hashlib.md5()
    hasha = argv.get("hash")

    # check if its an valid hashing
    if hasha in hashlib.algorithms_available:
        if not hasha in hashlib.algorithms_guaranteed:
            # warning
            pass
        hashIs = hashlib.new(hasha)

    else:
        hashIs = hashlib.md5()
    
    toCheck = argv.get("check")

    if not toCheck in (None, True):
        if os.path.exists(toCheck):
            co = argv.get("color")
            check(toCheck, hashIs, co)

        else:
            print("File does not exist")
            exit() 
    
    else:
        outfile = argv.get("output")
        useOut = False
        output = None

        if not outfile == None:
            useOut = True
            output = open(outfile, "w")
        else:
            useOut = False

        # check path
        N_path = argv.get("path")

        if not N_path == None:
            M_path = N_path.replace("\\", "/")


        # walk directory
        for path, subdirs, files in os.walk(M_path):
            # for each file
            for name in files:
                # add it to FILES list() 
                FILES.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))
        
        # go over files and hash them all
        for fname in FILES:
            try:
                i = str(hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashIs)) + " " + str(fname)
            except Exception as e:
                # skip
                print(e)
                continue

            # if the last arguemnt is true then remove fullpath
            if len(args) >= 1 and not useOut:
                if args[len(args) - 1] == "True":
                    print(i.replace(M_path, "."))
                else:
                    # if there if more than one argument
                    print(i)
                    pass
            
            elif useOut and output != None:
                output.write(i + "\n")
                pass
                
            else:
                print(i)
                pass

if __name__ == "__main__":
    main()