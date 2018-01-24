"""Command line program for hashit

this module "__main__" contains all the code for argparsing, running
and anything needed for an command lin application such as hashit.

it uses argc another package by me, but i am considering switching to argparse
"""
import json
import random
import argparse
# Import all from hashit
from .__init__ import os, hashlib, eprint, hashFile, new, bsd_tag, load, \
    GLOBAL, Exit, check, generate_data_set, detect, sfv_max, fixpath, \
    __algorithms__, __author__, __help__, __license__, supports_color

from .extra import LINUX_LIST
from .version import __version__

class Print(argparse.Action):
    """Print action for argparse, takes one kwarg which is text the varible which contains the string to be printed"""
    def __init__(self, nargs=0, **kwargs):
        if nargs != 0:
            raise ValueError('nargs for Print must be 0; it is just a flag.')
        elif "text" in kwargs:
            self.data = kwargs.pop("text")

        super(Print, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.data)

class Execute(argparse.Action):
    """Same as Print() but instead of printing an object it calls it takes func (function), and exit (bool)"""
    def __init__(self, nargs=0, **kwargs):
        if nargs != 0:
            raise ValueError('nargs for Execute must be 0; it is just a flag.')
        
        if "func" in kwargs:
            self.data = kwargs.pop("func")

        if "exit" in kwargs:
            self.exit = True if kwargs.pop("exit") else False

        super(Execute, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.data())
        if self.exit:
            exit()

def walk(go_over):
    """Goes over a path an finds all files, appends them to a list and returns that list"""
    walked = []
    for path, _subdirs, files in os.walk(go_over):
        # for each file
        for name in files:
            # add it to in_files list()
            walked.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))

    # return list with file names
    return walked

def config(parser):
    """Sets argvs' config and commands with argparse and returns it for good sake"""

    def hash_list():
        """Generates an easy-to-read list"""
        algos = set((__algorithms__ + ["sha3_224", "sha3_256", "sha3_384", "sha3_512"] if os.sys.version_info[0] == 3 else __algorithms__)\
             + list(GLOBAL["EXTRA"].keys())) # add extras
        # sort set
        s = [sorted(algos)[x:x+2] for x in range(0, len(algos), 2)]
        for c, l in enumerate(s):
            s[c] = ', '.join(l)

        return  "\n" + '\n'.join(s) + "\n"

    # set commands
    parser.add_argument('path', nargs="?", default=os.getcwd()) # for directroy
    parser.add_argument("-V", "--version", help="Print current version and exit", action="version", version="%(prog)s " + __version__)
    parser.add_argument("-l", "--license", help="Print license and exit", action=Print, text=__license__)
    parser.add_argument("-H", "--hash", help="Select hash use -hl --hash-list for more info", metavar="hashname", default=GLOBAL["DEFAULTS"]["HASH"])
    parser.add_argument("-hl", "--hash-list", help="Prints list of all supported hashes and exits", action=Execute, func=hash_list, exit=True)
    parser.add_argument("-a", "--all", help="Calculate all hashes for a single file", metavar="filename")
    parser.add_argument("-C", "--color", help="Enable colored output where it is supported", action="store_true", default=GLOBAL["DEFAULTS"]["COLORS"])
    parser.add_argument("-f", "--file", help="Hash single a file", metavar="filename")
    parser.add_argument("-S", "--size", help="Adds the file size to the output", action="store_true", default=GLOBAL["DEFAULTS"]["SIZE"])
    parser.add_argument("-s", "--string", nargs="?", help="hash a string or a piece of text", default=False)
    parser.add_argument("-sp", "--strip-path", help="Strips fullpath from the results", action="store_true", default=GLOBAL["DEFAULTS"]["STRIP"])
    parser.add_argument("-A", "--append", help="Instead of writing to a file you will append to it", action="store_true", default=GLOBAL["DEFAULTS"]["APPEND"])
    parser.add_argument("-d", "--detect", nargs="?", help="Enable hash detection for check", default=GLOBAL["DEFAULTS"]["DETECT"])
    parser.add_argument("-c", "--check", help="Verify checksums from a checksum file", metavar="filename", default=GLOBAL["DEFAULTS"]["MEMOPT"])
    parser.add_argument("-o", "--output", help="output output to an output (file)", metavar="filename")
    parser.add_argument("-q", "--quiet", help="Reduces output", action="store_true")
    parser.add_argument("-m", "--memory-optimatation", help="Enables memory optimatation (useful for large files)", action="store_true")
    parser.add_argument("-sfv", "--sfv", help="Outputs in a sfv compatible format", action="store_true")
    parser.add_argument("-bsd", "--bsd", help="output using the bsd checksum-format", action="store_true")
    parser.add_argument("-r", "--recursive", help="Hash all files in all subdirectories", action="store_true", default=GLOBAL["DEFAULTS"]["RECURS"])
    # return parser
    return parser

def main_(args=None):
    """Main function which is the cli parses arguments and runs appropriate commands"""
    # switch args if needed
    if args is None:
        # to sys.args
        args = os.sys.argv[1:]
    # using argparse instead of argc for portability
    parser = argparse.ArgumentParser("hashit", description=__help__, epilog=__license__)
    # set commands and config with config
    parser = config(parser)

    # check for amount of arguments
    if len(args) == 0:
        # if there is not arguments show help
        parser.parse_args(["--help"])

    # parse args
    argv = parser.parse_args(args)

    # Varibles

    # set colors
    RED = ""
    GREEN = ""
    YELLOW = ""
    RESET = ""

    # check if we should use colors
    if supports_color() and argv.color:
        # if yes enable them
        RED = GLOBAL["COLORS"]["RED"]
        GREEN = GLOBAL["COLORS"]["GREEN"]
        YELLOW = GLOBAL["COLORS"]["YELLOW"]
        RESET = GLOBAL["COLORS"]["RESET"]

    # file list, and path
    in_files = list() # list of all files
    my_path = os.getcwd() # path to search in

    # use md5 by default
    hash_is = new(GLOBAL["DEFAULTS"]["HASH"])

    # check if its an valid hashing
    if argv.hash in hashlib.algorithms_available or argv.hash in __algorithms__ or argv.hash in list(GLOBAL["EXTRA"].keys()) or str(argv.hash)[:5] == "shake":
        # check if it's in guaranteed
        if not argv.hash in hashlib.algorithms_guaranteed and argv.hash in hashlib.algorithms_available:
            # if not print an warning
            if not argv.quiet:
                eprint(YELLOW + str(argv.hash), GLOBAL["MESSAGES"]["WORKS_ON"] + RESET)
        # and use the hash
        hash_is = new(argv.hash)

    elif not argv.hash in GLOBAL["BLANK"]:
        # then print error messageh
        eprint(RED + str(argv.hash), GLOBAL["MESSAGES"]["HASH_NOT"], RESET)

    # select output
    use_out = False
    output = None

    # check if out is set and it has a value
    if not argv.output in GLOBAL["BLANK"]:
        # if it is open file
        use_out = True
        output = open(fixpath(argv.output), GLOBAL["WRITE_MODE"])
    else:
        # else set it to false
        use_out = False

    

    # check for new path
    if len(args) >= 1:
        new_path = argv.path
        # check if argument is path else do not change path
        if os.path.exists(new_path) and ("/" in new_path or new_path in (".", "..")):
            my_path = new_path
    if "-d" in args or "--detect" in args:
        argv.detect = True

    # check for string
    if "-s" in args or "--string" in args:
        data = argv.string
        if not data:
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
    elif not argv.all in GLOBAL["BLANK"]:
        if os.path.exists(argv.all):
            data = open(argv.all, "rb").read()
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
    elif not argv.detect in GLOBAL["BLANK"]:
        hashes = detect(argv.detect, generate_data_set("Hallo", __algorithms__, new))
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
    elif argv.check:
        # check for file
        if os.path.exists(argv.check):
            # then check
            check(
                argv.check,
                hash_is,
                argv.color,
                argv.quiet,
                argv.detect,
                argv.sfv,
                argv.size,
                argv.bsd
            )

        else:
            # if the file does not exist
            # print error message
            eprint(RED + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)
            Exit(1) # and exit

    # check the argv.file argument
    elif not argv.file in GLOBAL["BLANK"]:
        in_files = [argv.file]

    elif argv.recursive:
        # walk directory and add files to my_path
        in_files = walk(my_path)
    else:
        # else just hash the files in this directory
        in_files =  [my_path + "/" + f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]

    # if there is any files in in_files
    if in_files: 
        # find the longest filename
        longest_filename = max(in_files, key=len)

        # go over files and hash them all
        for fname in in_files:
            try:
                # hash file
                current_hash = hashFile(fname, hash_is, argv.memory_optimatation)

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

            if argv.size:
                size = str(os.stat(fname).st_size)

            if argv.sfv:
                print_str = sfv_max(current_hash, fname, len(longest_filename), size + " ")

            elif argv.bsd:
                print_str = bsd_tag(current_hash, fname, hash_is.name) + " "  + size

            else:
                print_str = current_hash + " " + str(size + " " + fname)

            # check if fullpath path shall be stripped
            if argv.strip_path:
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

    this main function calls main_() and cathes any error while giving the user some "pretty"
    errors.
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