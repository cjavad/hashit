"""Commandline code for hashit application"""
from argc import argc
# Import all from hashit
from .__init__ import os, hashlib, eprint, hashFile, \
    GLOB_CONFIG, Exit, check, generate_data_set, detect, sfv_max, \
    __algorithems__, __author__, __help__, __license__

from .version import __version__

def main(args=None):
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
    argv.set("-sp", "--strip-path", "spath", "Strips fullpath from results", False)
    argv.set("-c", "--check", "check", "Check checksum-file (sfv or standard)", None)
    argv.set("-o", "--output", "output", "Output data to file (in->do->out)", None)
    argv.set("-C", "--color", "color", "Enable colored output where it is supported", False)
    argv.set("-d", "--detect", "detect", "Enable hash detection for check and if you pass it and hash it will detect that", None)
    argv.set("-f", "--file", "file", "Hash single a file", None)
    argv.set("-q", "--quiet", "quiet", "Minimal output", False)
    argv.set("-m", "--memory-optimatation", "memopt", "Enables memory optimatation only useful for large files", False)
    argv.set("-sfv", "--simple-file-verification", "sfv", "Outputs in a sfv compatible format", False)

    # run (can raise SystemExit)
    argv.run()

    ''' Varibles '''
    # set colors
    RED = GLOB_CONFIG["COLORS"]["RED"]
    GREEN = GLOB_CONFIG["COLORS"]["GREEN"]
    RESET = GLOB_CONFIG["COLORS"]["RESET"]

    # file list, and path
    in_files = list() # list of all files
    my_path = os.getcwd() # path to search in

    # get hash from arguments
    # default is md5 for now
    hasha = argv.get("hash")
    # it supports md5 and sha256
    hash_is = hashlib.md5()

    # check if its an valid hashing
    if hasha in hashlib.algorithms_available:
        # check if it's in guaranteed
        if not hasha in hashlib.algorithms_guaranteed:
            # if not print an warning
            eprint(hasha, "is not guaranteed to work on your system")
        # and use the hash
        hash_is = hashlib.new(hasha)

    else:
        # else set it to md5
        hash_is = hashlib.md5()

    # get all other options and parse them
    to_detect = argv.get("detect") # to detect or not
    to_check = argv.get("check") # to check or not
    hash_onefile = argv.get("file") # only hash a single file (md5sum behavior)
    use_colors = argv.get("color") # use colors
    be_quiet = argv.get("quiet") # silent output
    to_strippath = argv.get("spath") # strip fullpath
    output_file = argv.get("output") # output output to output (in->do->out)
    use_sfv = argv.get("sfv") # use simple file verification compatible format
    use_mem = argv.get("memopt") # use memory optimatations

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
        my_path = new_path.replace("\\", "/") if os.path.exists(new_path) else my_path
    
    # if detect is choosen use it
    if not to_detect in (None, True):
        hashes = detect(to_detect, generate_data_set("Hallo", __algorithems__))
        for item in hashes.certain:
            print("Same results as", item)

        # print sepetator
        print("")

        for item in hashes.maybe:
            print("Maybe", item)
        # exit when done
        Exit()

    # if to check use that
    elif not to_check in (None, True):
        # check for file
        if os.path.exists(to_check):
            # then check
            check(to_check, hash_is, use_colors, be_quiet, to_detect, use_sfv)

        else:
            # if the file does not exist
            # print error message
            eprint(GLOB_CONFIG["FILE_NOT"])
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
            if use_sfv:
                print_str = sfv_max(current_hash, fname, len(longest_filename))
            else:
                print_str = current_hash + " " + str(fname)

            # if the last arguemnt is true then remove fullpath
            if len(args) >= 1 and not use_out:

                if to_strippath:
                    print(print_str.replace(my_path, "."))
                else:
                    # if there if more than one argument
                    print(print_str)

            # if we should output the result to a file
            elif use_out and output != None:
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

if __name__ == "__main__":
    main()
