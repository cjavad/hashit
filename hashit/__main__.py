"""Commandline code for hashit application"""
import json
from argc import argc
# Import all from hashit
from .__init__ import os, hashlib, eprint, hashFile, new, \
    CONFIG, Exit, check, generate_data_set, detect, sfv_max, \
    __algorithems__, __author__, __help__, __license__, supports_color

from .version import __version__

def _main(args=None):
    """Main function which is the cli parses arguments and runs appropriate commands"""
    # switch args if needed
    if args is None:
        # to sys.args
        args = os.sys.argv[1:]

    # using argc module by me (support for python2)
    argv = argc(args, False)
    # set commands
    argv.set("-h", "--help", "help", "Print help message", None, __help__(argv.generate_docs), True)
    argv.set("-v", "--version", "version", "Print current version", None, __version__, True)
    argv.set("-l", "--license", "license", "Prints license", None, __license__, True)
    argv.set("-hl", "--hash-list", "hashlist", "Prints list of all supported hashes", None, "\nList of hashes:\n\n      " +  '\n      '.join(__algorithems__), True)
    # set arguments
    argv.set("-H", "--hash", "hash", "Select hash use -hl --hash-list for more info", None)
    argv.set("-a", "--all", "all", "Calculate all hashes posible for a single file and output as json", None)
    argv.set("-sp", "--strip-path", "spath", "Strips fullpath from results", False)
    argv.set("-c", "--check", "check", "Check checksum-file (sfv or standard)", None)
    argv.set("-o", "--output", "output", "Output data to file (in->do->out)", None)
    argv.set("-C", "--color", "color", "Enable colored output where it is supported", CONFIG["USE_COLORS_DEFAULT"])
    argv.set("-d", "--detect", "detect", "Enable hash detection for check and if you pass it and hash it will detect that", None)
    argv.set("-f", "--file", "file", "Hash single a file", None)
    argv.set("-q", "--quiet", "quiet", "Minimal output", False)
    argv.set("-m", "--memory-optimatation", "memopt", "Enables memory optimatation only useful for large files", False)
    argv.set("-sfv", "--simple-file-verification", "sfv", "Outputs in a sfv compatible format", False)
    argv.set("-s", "--size", "size", "Adds a size to output", False)

    if len(args) == 0:
        # if there is not arguments show help
        argv.args["--help"] = True
    # run (can raise SystemExit)
    argv.run()


    """ Varibles """
    # set colors
    RED = CONFIG["COLORS"]["RED"]
    GREEN = CONFIG["COLORS"]["GREEN"]
    YELLOW = CONFIG["COLORS"]["YELLOW"]
    RESET = CONFIG["COLORS"]["RESET"]


    # file list, and path
    in_files = list() # list of all files
    my_path = os.getcwd() # path to search in

    # get hash from arguments
    # default is md5 for now
    hasha = argv.get("hash")
    # get all other options and parse them
    to_detect = argv.get("detect") # to detect or not
    to_check = argv.get("check") # to check or not
    hash_onefile = argv.get("file") # only hash a single file (md5sum behavior)
    all_onefile = argv.get("all")
    use_colors = argv.get("color", True) # use colors (True for detect type)
    be_quiet = argv.get("quiet") # silent output
    to_strippath = argv.get("spath") # strip fullpath
    output_file = argv.get("output") # output output to output (in->do->out)
    use_sfv = argv.get("sfv") # use simple file verification compatible format
    use_mem = argv.get("memopt") # use memory optimatations
    use_size = argv.get("size") # get size of file in bytes

    # it supports md5 and sha256
    hash_is = hashlib.md5()

    # check if its an valid hashing
    if hasha in hashlib.algorithms_available or hasha in __algorithems__ or str(hasha)[:5] == "shake":
        # check if it's in guaranteed
        if not hasha in hashlib.algorithms_guaranteed and hasha in hashlib.algorithms_available:
            # if not print an warning
            if not be_quiet:
                eprint(YELLOW + str(hasha), "is not guaranteed to work on your system" + RESET)
        # and use the hash
        hash_is = new(hasha)

    else:
        if not hasha in (None, True) and not be_quiet:
            eprint(RED + str(hasha), "is not a valid hash", RESET)
        # else set it to md5
        hash_is = hashlib.md5()

    # select output
    use_out = False
    output = None

    # check if out is set and it has a value
    if not output_file in (None, True):
        # if it is open file
        use_out = True
        output = open(output_file, "w")
    else:
        # else set it to false
        use_out = False


    # check for new path
    if len(args) >= 1:
        new_path = args[len(args) - 1]
        # check if argument is path else do not change path
        my_path = new_path.replace("\\", "/") if os.path.exists(new_path) and \
            (new_path.count("/") >= 1 or new_path in (".", "..")) else my_path

    # check if we should use colors
    if supports_color() ^ use_colors:
        # if not disable them
        RED = ""
        GREEN = ""
        YELLOW = ""
        RESET = ""
    
    # check for hash one file
    if not all_onefile in (None, True):
        if os.path.exists(all_onefile):
            data = open(all_onefile, "rb").read()
            results = {}
            for algo in __algorithems__:
                results[algo] = new(algo, data).hexdigest()

            out = json.dumps(results, indent=4, sort_keys=True)

            if use_out and output != None:
                output.write(out)
            else:
                print(out)
        else:
            eprint(RED + CONFIG["FILE_NOT"] + RESET)

    # if detect is choosen use it
    elif not to_detect in (None, True):
        hashes = detect(to_detect, generate_data_set("Hallo", __algorithems__, new))
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
        Exit()

    # if to check use that
    elif not to_check in (None, True):
        # check for file
        if os.path.exists(to_check):
            # then check
            check(to_check, hash_is, use_colors, be_quiet, to_detect, use_sfv, use_size)

        else:
            # if the file does not exist
            # print error message
            eprint(RED + CONFIG["FILE_NOT"] + RESET)
            Exit() # and exit

    # check the hash_onefile argument
    elif not hash_onefile in (None, True):
        in_files.append(hash_onefile)

    else:
        # walk directory and add files to my_path
        for path, _subdirs, files in os.walk(my_path):
            # for each file
            for name in files:
                # add it to in_files list()
                in_files.append((path  + "/" + name).replace("\\", "/").replace("//", "/"))

    # if there is any files in in_files
    if in_files: 
        # find the longest filename
        longest_filename = max(in_files, key=len)

        # go over files and hash them all
        for fname in in_files:
            try:
                # hash file
                current_hash = hashFile(fname, hash_is, use_mem)

            except (FileNotFoundError, PermissionError) as Error:
                if Error == PermissionError:
                    eprint()
                # and continue
                continue
            
            # set print_str
            print_str = current_hash
            size = ""

            if use_size:
                size = str(os.stat(fname).st_size) + " "

            if use_sfv:
                print_str = sfv_max(current_hash, fname, len(longest_filename), size)
            else:
                print_str = current_hash + " " + str(size + fname)

            # check if fullpath path shall be stripped
            if to_strippath:
                print_str = print_str.replace(my_path, ".") 
            
            # if we should output the result to a file
            if use_out and output != None:
                # write result to an file
                output.write(print_str + "\n")

            else:
                # else print it
                print(print_str)

        # Exit when done
        Exit()
    else:
        # Else exit
        Exit()

def main(args=None):
    """Main function that calls _main"""
    try:
        _main(args)
    except Exception as Error:
        # define colors
        RED = ""
        YELLOW = ""
        RESET = ""
        # check if term supports color
        if supports_color():
            YELLOW = CONFIG["COLORS"]["YELLOW"]
            RED = CONFIG["COLORS"]["RED"]
            RESET = CONFIG["COLORS"]["RESET"]

        if type(Error) == KeyboardInterrupt:
            pass
        elif type(Error) == TypeError:
            eprint(YELLOW + "Wrong type used (in cli-arguments) - please use a static programming language" + RESET)
        else:
            eprint(RED + str(Error) + RESET)
        Exit()

if __name__ == "__main__":
    main()
