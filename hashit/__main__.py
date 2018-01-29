"""Command line application for hashit

this module "__main__" contains all the code for argparsing, running
and anything needed for an command lin application such as hashit.

it uses argc another package by me, but i am considering switching to argparse
"""
import random
import traceback
import argparse
# Import all from hashit
from .__init__ import os, hashlib, eprint, hashFile, new, BSD, load, \
    GLOBAL, Exit, check, generate_data_set, detect, SFV, fixpath, \
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

        if "exit" in kwargs:
            self.exit = True if kwargs.pop("exit") else False

        super(Print, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.data)

        if self.exit:
            Exit(0)

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
            Exit(0)

def walk(go_over):
    """Goes over a path an finds all files, appends them to a list and returns that list"""
    walked = []
    for path, _subdirs, files in os.walk(go_over):
        # if the path does not exist skip it (What)
        if not os.path.exists(path):
            continue
        # for each file
        for name in files:
            # add it to in_files list() if it does exist
            p = (path  + "/" + name).replace("\\", "/").replace("//", "/")
            if os.path.exists(p):
                walked.append(p)

    # return list with file names
    return walked

# exclude function faster then last implementation
def exclude(items, excludes):
    """Exclude removes all items in a list that is in the excludes list (for dirs)"""

    for ex in excludes:
        items = [x for x in items if not ex in x]
    # return items
    return items

def config(parser):
    """Sets argvs' config and commands with argparse and returns it for good sake"""

    def hash_list():
        """Generates an easy-to-read list"""
        algos = set((__algorithms__ + list(GLOBAL["EXTRA"].keys()))) # add extras
        # sort set
        s = [sorted(algos)[x:x+2] for x in range(0, len(algos), 2)]
        for c, l in enumerate(s):
            s[c] = ', '.join(l)

        return  "\n" + '\n'.join(s) + "\n"
    
    def help_self():
        """Launches help() for module"""
        # get info from self
        help(os.sys.modules["hashit"])
        help(os.sys.modules[__name__]) # current
        help(os.sys.modules["hashit.detection"])
        help(os.sys.modules["hashit.extra"])
        help(os.sys.modules["hashit.version"])

        return __help__

    # create groups
    ghelp = parser.add_argument_group("help")
    formats = parser.add_argument_group("formats")
    settings = parser.add_argument_group("settings")
    other = parser.add_argument_group("other")
    dev = parser.add_argument_group("devtools")

    # set commands
    parser.add_argument('path', nargs="?", default=os.getcwd()) # for directroy
    parser.add_argument("files", nargs="*", default=[]) # for a list of files

    # add all the helping arguments
    ghelp.add_argument("-h", "--help", help="show this help message and exit", action=Execute, func=parser.format_help, exit=True)
    ghelp.add_argument("-p", "--page", help="Launch interactive help with python help() (for python api)", action=Execute, func=help_self, exit=True)
    ghelp.add_argument("-V", "--version", help="Print current version and exit", action="version", version="%(prog)s " + __version__)
    ghelp.add_argument("-l", "--license", help="Print license and exit", action=Print, text=__license__, exit=True)
    ghelp.add_argument("-hl", "--hash-list", help="Prints list of all supported hashes and exits", action=Execute, func=hash_list, exit=True)

    # all the options that sets something
    settings.add_argument("-H", "--hash", help="Select hash use -hl --hash-list for more info", metavar="hashname", default=GLOBAL["DEFAULTS"]["HASH"])
    settings.add_argument("-e", "--exclude", help="list of files and directories to exclude", default=[], metavar="excludes", nargs="+")
    settings.add_argument("-C", "--color", help="Enable colored output where it is supported", action="store_true", default=GLOBAL["DEFAULTS"]["COLORS"])
    settings.add_argument("-sp", "--strip-path", help="Strips fullpath from the results", action="store_true", default=GLOBAL["DEFAULTS"]["STRIP"])
    settings.add_argument("-A", "--append", help="Instead of writing to a file you will append to it", action="store_true", default=GLOBAL["DEFAULTS"]["APPEND"])
    settings.add_argument("-q", "--quiet", help="Reduces output", action="store_true")
    settings.add_argument("-m", "--memory-optimatation", help="Enables memory optimatation (useful for large files)", action="store_true")
    settings.add_argument("-r", "--recursive", help="Hash all files in all subdirectories", action="store_true", default=GLOBAL["DEFAULTS"]["RECURS"])

    # other, things that are optinional such as detect and string hashes
    # other.add_argument("-a", "--all", help="Calculate all hashes for a single file", metavar="filename") NOTE: Removed for now
    other.add_argument("-s", "--string", nargs="?", help="hash a string or a piece of text", default=False, metavar="string")
    other.add_argument("-d", "--detect", nargs="?", help="Enable hash detection for check", metavar="hash", default=GLOBAL["DEFAULTS"]["DETECT"])
    # ~ More important ~
    other.add_argument("-c", "--check", help="Verify checksums from a checksum file", metavar="filename", default=GLOBAL["DEFAULTS"]["MEMOPT"])
    other.add_argument("-o", "--output", help="output output to an output (file)", metavar="filename")

    # ~ Formatting ~
    formats.add_argument("-S", "--size", help="Adds the file size to the output", action="store_true", default=GLOBAL["DEFAULTS"]["SIZE"])
    formats.add_argument("-sfv", "--sfv", help="Outputs in a sfv compatible format", action="store_true")
    formats.add_argument("-bsd", "--bsd", help="output using the bsd checksum-format", action="store_true")

    # ~ Devtools ~
    dev.add_argument("--trace", help="Print traceback of any error cathed and exit", action="store_true", default=GLOBAL["DEFAULTS"]["TRACE"])
    dev.add_argument("--strict", help="Exit non-zero on any errors", action="store_true", default=GLOBAL["DEFAULTS"]["STRICT"])

    # return parser
    return parser

def main_(args):
    """Main function which is the cli parses arguments and runs appropriate commands"""
    # using argparse instead of argc for portability
    parser = argparse.ArgumentParser("hashit", description=__help__, epilog=__license__, add_help=False)
    # set commands and config with config
    parser = config(parser)

    # check for amount of arguments
    if not args:
        # if there is not arguments show help
        parser.parse_args(GLOBAL["IF_NO_ARGS"])

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
    if os.path.isdir(argv.path):
        new_path = argv.path
        # check if argument is path else do not change path
        if os.path.exists(new_path) and ("/" in new_path or new_path in (".", "..")):
            my_path = new_path

    """ NOTE: Removed all for now
    # check for hash one file
    if not argv.all in GLOBAL["BLANK"]:
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
    """

    # check for string in args needed because argparse
    # does not support both store_true and store same for detect
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

    # if detect is choosen use it
    elif not argv.detect in GLOBAL["BLANK"]:
        hashes = detect(argv.detect, generate_data_set("Hallo", __algorithms__, new))
        if hashes != None:
            for item in hashes.certain:
                print(GREEN + GLOBAL["MESSAGES"]["RESULTS_AS"], item + RESET)

            # print sepetator if there is a need for one
            if hashes.maybe and hashes.certain:
                print("")

            for item in hashes.maybe:
                print(YELLOW + GLOBAL["MESSAGES"]["MAYBE"], item + RESET)
        else:
            print(RED + str(argv.detect) + " " + GLOBAL["MESSAGES"]["HASH_NOT"] + RESET)

    # if to check use that
    elif argv.check:
        # set argv.detect to true
        if "-d" in args or "--detect" in args:
            argv.detect = True
        # check for file
        if os.path.exists(argv.check):
            # then check
            return check(
                argv.check,
                hash_is,
                argv.color,
                argv.quiet,
                argv.detect,
                argv.sfv,
                argv.size,
                argv.bsd,
                argv.strict
            )

        else:
            # if the file does not exist
            # print error message
            eprint(RED + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)

            if argv.strict:
                return 1 # and exit non-zero

            # Else return 0
            return 0 

    # ~ Check for files ~

    # check the argv.files argument, and the path var
    # which can be a file.
    elif argv.files or os.path.isfile(argv.path):
        for f in argv.files + [argv.path]:
            p = fixpath(f) # use fixpath
            if os.path.exists(p):
                # if path is file
                if os.path.isfile(p):
                    # append to in_files
                    in_files.append(p)
            else:
                # if file not exist then print error
                eprint(RED + "{}, ".format(p) + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)
                # if strict exit non-zero
                if argv.strict:
                    return 1

                # else return zero
                return 0

    # else if my_path is a dir and r is true
    elif argv.recursive and os.path.isdir(my_path):
        # walk directory and add files to my_path
        in_files = walk(my_path)

    # else if my_path is a dir then just
    elif os.path.isdir(my_path):
        # hash all of the files in this directory
        in_files =  [os.path.join(my_path, f) for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]

    # if there is any files in in_files
    if in_files:
        # check if we should remove any files
        if argv.exclude:
            # exclude files and fix paths
            in_files = exclude([fixpath(f) for f in in_files], argv.exclude)


            if not in_files:
                # no more files in in_files
                return 0

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
                    eprint(RED + fname + ", " + GLOBAL["MESSAGES"]["PERM_ERR"] + RESET)

                # print stack and trace if needed
                if argv.trace:
                    eprint(YELLOW, end="")
                    traceback.print_stack(file=os.sys.stderr)
                    traceback.print_exc(file=os.sys.stderr)
                    eprint(RESET, end="")

                continue

            # set print_str
            print_str = current_hash
            size = ""

            # size override size as string
            if argv.size:
                size = str(os.stat(fname).st_size)

            # if sfv format string
            if argv.sfv:
                print_str = SFV.format(current_hash, fname, len(longest_filename), size)
            # is bsd format string
            elif argv.bsd:
                print_str = BSD.format(current_hash, fname, hash_is.name) + (size if len(size) <= 0 else " " + size)
            # else use N/A
            else:
                print_str = current_hash + " " + str(size + " " + fname)

            # check if fullpath path shall be stripped
            if argv.strip_path:
                # then replace current path with .
                print_str = print_str.replace(os.getcwd(), ".")

            # if we should output the result to a file
            if use_out and output != None:
                # write result to an file
                output.write(print_str + "\n")

            else:
                # else print it
                print(print_str)

    # return ExitCode
    return 0

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
    # switch args if needed
    if args is None:
        # to sys.args
        args = os.sys.argv[1:]
    try:
        # execute main application
        Exit(main_(args)) # Exit with return code
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

        elif isinstance(error, ValueError):
            eprint(YL + GLOBAL["ERRORS"]["ValueError"] + RE)

        elif isinstance(error, FileNotFoundError):
            eprint(YL + GLOBAL["ERRORS"]["FileNotFoundError"] + RE)

        elif isinstance(error, OSError):
            eprint(YL + GLOBAL["ERRORS"]["OSError"]["windows"])
            eprint(GLOBAL["ERRORS"]["OSError"]["macos"])
            eprint(GLOBAL["ERRORS"]["OSError"]["linux"].format(', '.join(random.sample(LINUX_LIST, 10))))
            eprint(GLOBAL["ERRORS"]["OSError"]["END"] + RE)

        # print stack and trace if needed
        if "--trace" in args or "-t" in args:
            eprint(RD, end="")
            traceback.print_stack(file=os.sys.stderr)
            traceback.print_exc(file=os.sys.stderr)
            eprint(RE, end="")
        else:
            # else print error
            eprint(RD + str(error) + RE)

        os._exit(1) # force exit

# if the program is being called
if __name__ == "__main__":
    # Exit 0 on KeyboardInterruptExit
    try:
        main() # then execute main function
    except KeyboardInterrupt:
        Exit(130) # According to the posix standard
