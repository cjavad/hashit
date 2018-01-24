"""Command line program for hashit

this module "__main__" contains all the code for argparsing, running
and anything needed for an command lin application such as hashit.

it uses argc another package by me, but i am considering switching to argparse
"""
import json
import random
from argc import argc
# Import all from hashit
from .__init__ import os, hashlib, eprint, hashFile, new, bsd_tag, load, \
    GLOBAL, Exit, check, generate_data_set, detect, sfv_max, fixpath, \
    __algorithms__, __author__, __help__, __license__, supports_color

from .extra import LINUX_LIST
from .version import __version__

def walk(goover):
    """Goes over a path an finds all files, appends them to a list and returns that list"""
    walked = []
    for path, _subdirs, files in os.walk(goover):
        # for each file
        for name in files:
            # add it to in_files list()
            walked.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))

    # return list with file names
    return walked

def config(argv):
    """Sets argvs' config and commands"""

    def hash_list():
        """Generates an easy-to-read list"""
        algos = set((__algorithms__ + ["sha3_224", "sha3_256", "sha3_384", "sha3_512"] if os.sys.version_info[0] == 3 else __algorithms__)\
             + list(GLOBAL["EXTRA"].keys())) # add extras
        # sort set
        s = [sorted(algos)[x:x+2] for x in range(0, len(algos), 2)]
        for c, l in enumerate(s):
            s[c] = ', '.join(l)

        return [""]+s+[""]

    # set commands
    argv.set("-h", "--help", "help", "Print help message and exit", None, __help__(argv.generate_docs), True)
    argv.set("-v", "--version", "version", "Print current version and exit", None, __version__, True)
    argv.set("-l", "--license", "license", "Print license and exit", None, __license__, True)
    argv.set("-hl", "--hash-list", "hashlist", "Prints list of all supported hashes and exits", None, hash_list(), True)
    # set arguments
    argv.set("-H", "--hash", "hash", "Select hash use -hl --hash-list for more info", GLOBAL["DEFAULTS"]["HASH"])
    argv.set("-a", "--all", "all", "Calculate all hashes posible for a single file and output as json")
    argv.set("-s", "--string", "str", "hash a string/text", False)
    argv.set("-sp", "--strip-path", "spath", "Strips fullpath from results", GLOBAL["DEFAULTS"]["STRIP"])
    argv.set("-c", "--check", "check", "Check checksum-file (sfv or standard)")
    argv.set("-o", "--output", "output", "Output data to file (in->do->out)")
    argv.set("-C", "--color", "color", "Enable colored output where it is supported", GLOBAL["DEFAULTS"]["COLORS"])
    argv.set("-d", "--detect", "detect", "Enable hash detection for check and if you pass it and hash it will detect that", GLOBAL["DEFAULTS"]["DETECT"])
    argv.set("-f", "--file", "file", "Hash single a file")
    argv.set("-q", "--quiet", "quiet", "Minimal output", GLOBAL["DEFAULTS"]["QUIET"])
    argv.set("-bsd", "--bsd-tag", "bsd", "create a BSD-style checksum", False)
    argv.set("-m", "--memory-optimatation", "memopt", "Enables memory optimatation only useful for large files", GLOBAL["DEFAULTS"]["MEMOPT"])
    argv.set("-sfv", "--simple-file-verification", "sfv", "Outputs in a sfv compatible format", False)
    argv.set("-S", "--size", "size", "Adds a size to output", GLOBAL["DEFAULTS"]["SIZE"])
    argv.set("-A", "--append", "append", "Instead of writing to a file you will append to it", GLOBAL["DEFAULTS"]["APPEND"])

def main_(args=None):
    """Main function which is the cli parses arguments and runs appropriate commands"""
    # switch args if needed
    if args is None:
        # to sys.args
        args = os.sys.argv[1:]

    # using argc module by me (support for python2)
    argv = argc(args, False)
    # set commands and config with config
    config(argv)

    if len(args) == 0:
        # if there is not arguments show help
        argv.args["--help"] = True
    # run (can raise SystemExit)
    argv.run()


    # Varibles

    # set colors
    RED = ""
    GREEN = ""
    YELLOW = ""
    RESET = ""

    # file list, and path
    in_files = list() # list of all files
    my_path = os.getcwd() # path to search in

    Config = {}
    # get hash from arguments
    # default is md5 for now
    Config["hash"] = argv.get("hash")
    # get all other options and parse them
    Config["detect?"] = argv.get("detect") # to detect or not
    Config["check?"] = argv.get("check") # to check or not
    Config["single"] = argv.get("file") # only hash a single file (md5sum behavior)
    Config["all_single"] = argv.get("all")
    Config["colors?"] = argv.get("color", True) # use colors (True for detect type)
    Config["quiet?"] = argv.get("quiet") # silent output
    Config["strip-path?"] = argv.get("spath") # strip fullpath
    Config["writeToFile"] = argv.get("output") # output output to output (in->do->out)
    Config["SimpleFileVerification"] = argv.get("sfv") # use simple file verification compatible format
    Config["BSDTag"] = argv.get("bsd") # create a BSD-style checksum
    Config["MemoryOptimatation"] = argv.get("memopt") # use memory optimatations
    Config["AddSize"] = argv.get("size") # get size of file in bytes
    Config["String?"] = argv.get("str") # get string/setting 

    # use md5 by default
    hash_is = new(GLOBAL["DEFAULTS"]["HASH"])

    # check if its an valid hashing
    if Config["hash"] in hashlib.algorithms_available or Config["hash"] in __algorithms__ or Config["hash"] in list(GLOBAL["EXTRA"].keys()) or str(Config["hash"])[:5] == "shake":
        # check if it's in guaranteed
        if not Config["hash"] in hashlib.algorithms_guaranteed and Config["hash"] in hashlib.algorithms_available:
            # if not print an warning
            if not Config["quiet?"]:
                eprint(YELLOW + str(Config["hash"]), GLOBAL["MESSAGES"]["WORKS_ON"] + RESET)
        # and use the hash
        hash_is = new(Config["hash"])

    else:
        if not Config["hash"] in GLOBAL["BLANK"] and not Config["quiet?"]:
            # then print error message
            eprint(RED + str(Config["hash"]), GLOBAL["MESSAGES"]["HASH_NOT"], RESET)

    # select output
    use_out = False
    output = None

    # check if out is set and it has a value
    if not Config["writeToFile"] in GLOBAL["BLANK"]:
        # if it is open file
        use_out = True
        output = open(fixpath(Config["writeToFile"]), GLOBAL["WRITE_MODE"])
    else:
        # else set it to false
        use_out = False


    # check if we should use colors
    if supports_color() and Config["colors?"]:
        # if yes enable them
        RED = GLOBAL["COLORS"]["RED"]
        GREEN = GLOBAL["COLORS"]["GREEN"]
        YELLOW = GLOBAL["COLORS"]["YELLOW"]
        RESET = GLOBAL["COLORS"]["RESET"]
    

    # check for new path
    if len(args) >= 1:
        new_path = args[len(args) - 1].replace("\\", "/")
        # check if argument is path else do not change path
        if os.path.exists(new_path) and ("/" in new_path or new_path in (".", "..")):
            my_path = new_path

    # check for string
    if not Config["String?"] == False:
        data = Config["String?"]
        if data == True:
            # reed from stdin like md5sum
            data = os.sys.stdin.read()

            # check if data ends with newline
            if not data.endswith("\n"):
                # else print one
                print("")

        # if the data isn't bytes
        if not isinstance(data, bytes):
            # encode it
            data = data.encode()

        # then hash-it
        hash_is.update(data)
        
        # check for output methods
        if use_out and output != None:
            output.write(hash_is.hexdigest())
        else:
            print(hash_is.hexdigest())

    # check for hash one file
    elif not Config["all_single"] in GLOBAL["BLANK"]:
        if os.path.exists(Config["all_single"]):
            data = open(Config["all_single"], "rb").read()
            results = {}
            for algo in __algorithms__:
                results[algo] = new(algo, data).hexdigest()

            out = json.dumps(results, indent=4, sort_keys=True)

            if use_out and output != None:
                output.write(out)
            else:
                print(out)
        else:
            eprint(RED + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)

    # if detect is choosen use it
    elif not Config["detect?"] in GLOBAL["BLANK"]:
        hashes = detect(Config["detect?"], generate_data_set("Hallo", __algorithms__, new))
        if hashes != None:
            for item in hashes.certain:
                print(GREEN + "Same results as", item + RESET)

            # print sepetator
            print("")

            for item in hashes.maybe:
                print(YELLOW + "Maybe", item + RESET)
        else:
            print(RED + "Not valid hash" + RESET)
        # exit when done
        Exit(0)

    # if to check use that
    elif not Config["check?"] in GLOBAL["BLANK"]:
        # check for file
        if os.path.exists(Config["check?"]):
            # then check
            check(
                Config["check?"],
                hash_is,
                Config["colors?"],
                Config["quiet?"],
                Config["detect?"],
                Config["SimpleFileVerification"],
                Config["AddSize"],
                Config["BSDTag"]
            )

        else:
            # if the file does not exist
            # print error message
            eprint(RED + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)
            Exit(1) # and exit

    # check the Config["single"] argument
    elif not Config["single"] in GLOBAL["BLANK"]:
        in_files = [Config["single"]]

    else:
        # walk directory and add files to my_path
        in_files = walk(my_path)

    # if there is any files in in_files
    if in_files: 
        # find the longest filename
        longest_filename = max(in_files, key=len)

        # go over files and hash them all
        for fname in in_files:
            try:
                # hash file
                current_hash = hashFile(fname, hash_is, Config["MemoryOptimatation"])

            except (FileNotFoundError, PermissionError) as Error:
                # if the file does not exist print a error message
                if isinstance(Error, FileNotFoundError):
                    eprint(RED + fname + ", " + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)

                # check if we have access to the file
                elif isinstance(Error, PermissionError):
                    eprint(RED + fname + " " + GLOBAL["MESSAGES"] + RESET)
                # and continue
                continue
            
            # set print_str
            print_str = current_hash
            size = ""

            if Config["AddSize"]:
                size = str(os.stat(fname).st_size)

            if Config["SimpleFileVerification"]:
                print_str = sfv_max(current_hash, fname, len(longest_filename), size + " ")

            elif Config["BSDTag"]:
                print_str = bsd_tag(current_hash, fname, hash_is.name) + " "  + size

            else:
                print_str = current_hash + " " + str(size + " " + fname)

            # check if fullpath path shall be stripped
            if Config["strip-path?"]:
                print_str = print_str.replace(my_path, ".") 
            
            # if we should output the result to a file
            if use_out and output != None:
                # write result to an file
                output.write(print_str + "\n")

            else:
                # else print it
                print(print_str)

        # Exit when done
        Exit(0)
    else:
        # Else exit
        Exit(1)

"""
Hashit __main__.py can be executed directly with python(3) -m hashit "commands"
and via snap
"""

def main(args=None):
    """
    Main function with error catching, can force-exit with os._exit(1)

    this main function calls main_() and cathes any error while giving the user a "pretty"
    error.
    """
    try:
        # execute main application
        main_(args)
    except Exception as error:
        # define colors
        RD = ""
        YL = ""
        RE = ""
        # check if term supports color
        if supports_color():
            YL = GLOBAL["COLORS"]["YELLOW"]
            RD = GLOBAL["COLORS"]["RED"]
            RE = GLOBAL["COLORS"]["RESET"]

        if isinstance(error, TypeError):
            eprint(YL + GLOBAL["ERRORS"]["TypeError"] + RE)

        elif isinstance(error, FileNotFoundError):
            eprint(YL + GLOBAL["ERRORS"]["FileNotFoundError"] + RE)
        
        elif isinstance(error, OSError):
            eprint(YL + GLOBAL["ERRORS"]["OSError"]["windows"])
            eprint(GLOBAL["ERRORS"]["OSError"]["macos"])
            eprint(GLOBAL["ERRORS"]["OSError"]["linux"].format(', '.join(random.sample(LINUX_LIST, 10))))
            eprint(GLOBAL["ERRORS"]["OSError"]["END"] + RE)

        # and print error
        eprint(RD + str(error) + RE)
        
        os._exit(1) # force exit

# if the program is being called
if __name__ == "__main__":
    main() # then execute main function
