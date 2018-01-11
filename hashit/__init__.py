# import print and with for python2 support
from __future__ import print_function, with_statement
import os
import hashlib
from .version import __version__ # global version
from .detect import detect, generate_data_set
from argc import argc


__author__ = "Javad Shafique" # copyrigth holder
__license__ = "MIT, Copyrigth (c) 2017-present Javad Shafique" # license foro program

# help message
# this list is the message that will be printed
# when the user uses hashit --help

# fix algo list
__algorithems__ = [s for s in hashlib.algorithms_available if not (str(s)[:5] in ("sha3_", "shake") or str(s)[:3] in ("SHA", "MD5", "MD4") or str(s) in ("RIPEMD160"))]

__help__ = [
    "Usage:\n",
    "   hashit [options] $extra",
    "",
    "Arguments:\n",
    "   -v --version: prints current version",
    "   -h --help: prints this message",
    "   -l --license: prints license",
    "   -p --path $path: sets path default $current",
    "   -H --hash $type: sets hash in a list use --hash-list or -hl",
    "   -c --check $filepath: reads output from this program and checks for change",
    "   -o --output $filepath: writes output to file same as '>' operator",
    "   -C --color: enables colored output. Only for check (-c, --check)",
    "   -q --quiet: prints the least output posible",
    "   -f --file: hashes a single file",
    "   -hl --hash-list: prints list of hashes",
    "   ",
    "   Use 'True' at the end for only outputting the releative path not the fullpath",
    "",
    "Notice: this program was made by Javad Shafique, and uses argc another package by me\n"
]

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=os.sys.stderr, **kwargs)

def einput(message):
    eprint(message, end="")
    m = str(os.sys.stdin.read())
    eprint("\n", end="")
    return m

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


def choose_hash(hash1, hashit):
    # check for valid 
    if hasattr(hashit, "name"):
        tup = detect(hash1, generate_data_set("Hallo", __algorithems__))

        # but only use if not already choosen
        if len(tup.certain) >= 1 and not (hashit.name in tup.certain or hashit.name in tup.maybe):
            hashit = hashlib.new(tup.certain[0])
        elif len(tup.maybe) >= 1:
            eprint("Did you maybe mean:")
            for c, h in enumerate(tup.maybe):
                eprint(h, "(" + str(c) + ")")
            ci = int(input())

            if len(tup.maybe) - 1 >= ci:  
                # choose maybe
                hashit = hashlib.new(tup.maybe[ci])
            else:
                eprint("To big a value")
        else:
            # choose certain
            eprint("Using", tup.certain[0])
            pass
    else:
        # else pass
        pass

    return hashit


# hashIter goes over an bytes string
# block for block and updates the hash while
# not having the intire file in memory

def hashIter(bytesiter, hashit, ashexstr=True):
    for block in bytesiter:
        hashit.update(block)
    return (hashit.hexdigest() if ashexstr else hashit.digest())

# blockIter creates bytestring-blocked
# byte data for hashIter

def blockIter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

# check reads an file generate with hashit > outfile
# and compares the results by re-hashing the file
# and print if there is a change

def check(path, hashit, color=False,  quiet=False):
    RED = "\x1b[0;31m"
    GREEN = "\x1b[0;32m"
    RESET = "\x1b[0m"

    # check if system supports color
    # with bitwise-exclusive or (XOR)
    if supports_color() ^ color:
        RED = ""
        GREEN = ""
        RESET = ""
    
    x = open(path, "r").readlines()

    # choose hash if not already selected
    # using new detection algorithem

    try:
        l1 = x[0].split(" ")
        hash1 = l1[0].replace("\n", "").replace("\0", "")
        hashit = choose_hash(hash1, hashit)
    except:
        # no data in file
        if len(x) <= 0:
            return

    # go over filedata
    for i in x:
        # split by spaces to get hash and filepath
        m = i.split(" ")
        
        # Wrong format
        if len(m) != 2:
            # then continue to next line
            continue
        
        # get hash and file path
        hashis = m[0].replace("\n", "").replace("\0", "")
        fname = m[1].replace("\n", "").replace("\0", "")

        try:
            # try to hash it again
            chash = str(hashIter(blockIter(open(fname, 'rb')), hashit))
        except:
            # print error
            print(RED + "Error while reading" + RESET, fname)
            continue # ehmm file does seem not exist

        if chash != hashis:
            # if the file has changed print notice (md5 sum inpired)
            print(fname + ":" + GREEN, hashis + RESET, ">", RED + chash, end=RESET + '\n')
        elif not quiet:
            # else print OK
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
    argv.set("-hl", "--hash-list", "hashlist", "Prints list of hashes", None, "\nList of hashes:\n\n      "+  '\n      '.join(__algorithems__), True)
    argv.set("-gh", "--generate-help", "ghelp", "Generates help from argc", None, argv.generate_docs, True)
    # set arguments
    argv.set("-H", "--hash", "hash", "Select hash", None)
    argv.set("-p", "--path", "path", "Path to scan", None)
    argv.set("-c", "--check", "check", "Check files", None)
    argv.set("-o", "--output", "output", "Output file", None)
    argv.set("-C", "--color", "color", "Set color true/false", False)
    argv.set("-d", "--detect", "detect", "Detect hash by string", None)
    argv.set("-f", "--file", "file", "Hash single file", None)
    argv.set("-q", "--quiet", "quiet", "Minimal output", False)

    # run (can raise SystemExit)
    argv.run()
    # Varibles
    FILES = list() # list of all files
    M_path = os.getcwd() # path to search in

    # get hash from arguments
    # default is md5 for now
    hasha = argv.get("hash")
    # it supports md5 and sha256
    hashIs = hashlib.md5()

    # check if its an valid hashing
    if hasha in hashlib.algorithms_available:
        if not hasha in hashlib.algorithms_guaranteed:
            eprint(hasha, "is not guaranteed to work on your system")
            pass
        hashIs = hashlib.new(hasha)

    else:
        hashIs = hashlib.md5()

    toDetect = argv.get("detect")
    toCheck = argv.get("check")
    oneFile = argv.get("file")
    quiet = argv.get("quiet")

    if not oneFile in (None, True):
        if os.path.exists(oneFile):
            h = str(hashIter(blockIter(open(oneFile, 'rb')), hashIs)) + " " + str(oneFile)

            outfile = argv.get("output")
            useOut = False
            output = None

            if not outfile == None:
                useOut = True
                output = open(outfile, "w")
            else:
                useOut = False
            if useOut:
                output.write(h)
            else:
                if args[len(args) - 1] == "True":
                   print(h.replace("M_path", ""))
                else:
                    print(h) 
        else:
            print("File does not exist")
        exit()
    
    if not toDetect in (None, True):
        hashes = detect(toDetect, generate_data_set("Hallo", __algorithems__))
        for item in hashes.certain:
            print("Same results as", item)
        
        for item in hashes.maybe:
            print("Maybe", item)

        exit()

    if not toCheck in (None, True):
        if os.path.exists(toCheck):
            co = argv.get("color")
            check(toCheck, hashIs, co, quiet)

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
                i = str(hashIter(blockIter(open(fname, 'rb')), hashIs)) + " " + str(fname)
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
