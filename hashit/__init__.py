"""hashit module for hashit command is contaning all the code for hashit

hashit is an hashing application which main purpose is to replace all the 'default'
hashing commands that comes with linux and also provide a usable hashing program
for windows hence the choice of using python. while hashit supports both python 2 and 3
i would strongly recommend using python3 because that python3 comes with a newer version
of hashlib and therefore many new hash-functions, altough it is posible to add these into
python2 with the load() function which acts like a 'connecter' and enables hashit to use
third-party hashing-functions as long as the have the same api as specified in docs/index.md

The GLOBAL dict contains all the configurations for this program, translations, error messages
settings, plugins and more.

__algorithms__ is a list that contains all the builtin algorithms including crc32

LICENSE:

    MIT License

    Copyright (c) 2018 Javad Shafique

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    NO ONE CAN CLAIM OWNERSHIP OF THIS "SOFTWARE" AND ASSOCIATED DOCUMENTATION FILES.
"""
# import print and with for python2 support
from __future__ import print_function, with_statement
import os
import re
import hashlib

from .extra import Crc32, shake
from .detection import detect, generate_data_set, ishex

__author__ = "Javad Shafique" # copyrigth holder
__license__ = "MIT, Copyrigth (c) 2017-2018 Javad Shafique" # license for the program

# help desciption
__help__ = """Hashit is an hashing program which can be uses to hash and verify
muliple files on a system. I got the idea from an ubuntu iso image which
have this hash table, so i got the idea to make such a program using
python.
"""

# fix algo list by sorting it trough (sha3_ is out because it interfears with the detection algoritm
__algorithms__ = sorted([s for s in hashlib.algorithms_available if not (s[:5] in ("shake") \
or s[:3] in {"SHA", "MD5", "MD4", "RIP"})] + ["crc32"], key=len) # add crc32 cause' it's a builtin

# Global config
GLOBAL = {
    "DEFAULTS":{
        "HASH":"md5", # default hash to use
        "STRIP":False,
        "COLORS":True, # if supported colors are on by default
        "MEMOPT":False,
        "SIZE":False,
        "TRACE":False,
        "STRICT":False,
        "QUIET":False,
        "DETECT":False,
        "APPEND":False,
        "RECURS":False
    },
    "EXTRA":{
        "crc32":Crc32
    },
    "COLORS":{
        "RED":"\x1b[0;31m",
        "GREEN":"\x1b[0;32m",
        "YELLOW":"\x1b[0;33m",
        "RESET":"\x1b[0m"
    },
    "MESSAGES":{
        "FILE_NOT":"File does not exist", # Warning when file dont exist
        "MAYBE_M":"Did you maybe mean:", # Message when selected new hash
        "HASH_NOT":"is not a valid hash", # Warning when hash is not loaded/exists
        "WRONG_FORMAT":"Checksum-file does not seem to be valid, maybe it is a sfv file? (try -sfv) or -S (size)", # warning when the file has a wrong format
        "EMPTY_CHK":"checksum file is empty", # Warning when check-file is empty
        "PERM_ERR":"could not be accessed", # Warning when we do not have access to a file
        "CUR_FORM":"current format is", # Message specifing the current fileformat (check)
        "WORKS_ON":"is not guaranteed to work on your system", # message when hash is not in hashlib.guaranteed
        "LOAD_FAIL":"Failed to load", # When failed to load a hashclass
        "OK":"OK", # OK message
        "FAIL":"FAILED", # FAIL message
        "MAYBE":"Maybe", # MAYBE Message
        "RESULTS_AS":"Same results as" # When results match
    },
    "ERRORS":{
        # JOKES in here
        "IndexError":"Out of range, cause i am not that big :)",
        "ValueError":"Wrong type or mood?! :)",
        "TypeError":"Wrong type used (in cli-arguments) - please use a static programming language",
        "FileNotFoundError":"Error, file seems to be missing calling systemd to confirm 'sure you haved checked the MBR?'",
        "OSError":{
            # set os-jokes here
            "windows":"Windows 10, windows 8(.1), windows 7 (sp*), windows vista (sp*), windows xp (sp*), windows 98/95, windows NT *. OK not that bad",
            "macos":"Macos (Sierra+) and OSX (El Captain-) thank god for apples naming",
            "linux":"So {} , to be continued...\n",
            "END":"JDK, so something happend with your os, message: "
        }
    },
    "IF_NO_ARGS":["--help"], # when no args is used this is the default setup
    "BLANK": (None, True, False),
    "SNAP_PATH":"/var/lib/snapd/hostfs",
    "PLATFORM":os.sys.platform,
    "DEVMODE":True,
    "ACCESS": (os.access("/home", os.R_OK) if os.path.exists("/home") else False),
    "HASH_STR":"Hello World!", # String that detect uses to generate the dataset
    "WRITE_MODE":"w" # 'w' not 'a'
}

# exit alias for sys.exit
Exit = os.sys.exit

# ~ Files ~

# gets fullpath
def fixpath(path):
    """Fixpath converts the releative path into an absolute path
    and if needed can append the path to the snap host-filesystem 
    which if the application is in devmode gives hashit access to 
    the hole filesystem, if you're not in devmode and you're still
    using snap, then you will need sudo to access the intire system.
    Also replaces / with \\ on windows"""
    c_path = os.path.join(os.getcwd(), path).replace("\\", "/")
    # check if you'll need to use snap
    if os.environ.get("SNAP") and GLOBAL["DEVMODE"] and not GLOBAL["ACCESS"]:
        c_path = GLOBAL["SNAP_PATH"] + c_path

    # check if we are on windows
    if GLOBAL["PLATFORM"] == "win32":
        c_path = c_path.replace("/", "\\")

    return c_path

def reader(filename, mode="r", comments=True):
    """Creates generator for an file, better for larger files not part of the MEMOPT,
    so an standard reader for most uses. Works like readlines but instead of a list it
    creates an generator that sortof clean the input before it is parsed by something like
    BSD() or SFV()."""
    filename = fixpath(filename)
    # return generator
    for line in open(filename, mode=mode).readlines():
        # if the line starts with and comments is enabled 
        if line.startswith(";") and comments:
            # then skip the line
            continue

        yield line.replace("\n", "")
    

# ~ File Formats ~

class SFV:
    """Class for parsing and creating sfv strings
    SFV() contains all functions needed for parsing,
    creating and formating SFV strings"""
    def __init__(self, filename=None, size=False):
        """Inits sfv class with file and use_size"""
        self.filename = filename
        self.size = size

    def read(self, filename=None, size=False):
        """Creates generator that reads and parses sfv compatible files using reader"""
        for line in reader(self.filename or filename, "r"):
            # read sfv file and create and generator with correct results
            yield self.parser(line, self.size or size)

    @staticmethod
    def format(file_hash, file_path, longest, size=""):
        """calculates the amount of spaces needed in a sfv file"""
        if size:
            # add size if so
            size = " " + size 
        # hardcoded space variable 
        spaces = " "
        # check length
        if len(file_path) - 1 < longest:
            # calculates the amount of spaces needed in a sfv file
            spaces = spaces*(longest - len(file_path) + 1)
        # return sfv compatible string
        return file_path + spaces + (file_hash + size)

    @staticmethod
    def parser(line, use_size=False):
        # split line by spaces
        line = str(line).strip().split(" ")
        # set size to None
        size = None

        # if size override size var with size
        if use_size:
            size = line.pop()

        # get hashstr and filename from list
        hashstr = line.pop()
        # remove spaces from list
        filename = ' '.join([l for l in line if l != ''])

        # return a list
        return [filename, hashstr] + ([size] if size != None else [])


class BSD:
    """Parser for bsd and formater, also the
    same as SFV() but BSD() instead of sfv uses
    the bsd checksum output which is like this:
        hashname (filename) = hash [size]"""
    def __init__(self, filename=None, size=False):
        """Inits bsd class with filename and use_size"""
        self.filename = filename
        self.size = size

    def read(self, filename=None, size=False):
        """Creates generator that reads and parses bsd strings"""
        for line in reader(self.filename or filename, "r"):
            yield self.parser(line, self.size or size)

    @staticmethod
    def format(file_hash, file_path, hashname):
        """Formats string in a bsd style format"""
        return "{} ({}) = {}".format(hashname, file_path, file_hash)

    @staticmethod
    def parser(line, use_size=False):
        """Parses bsd string"""
        # split line by spaces
        line = str(line).strip().split(" ") #[:-(0 + (not use_size))]
        line.remove("=")
        size = None

        if use_size:
            size = line.pop()
        # get hashname as the first 
        hashname = line[0]
        # get hashstring, by calculating its potition
        hashstr = line[len(line) - (1 + (not use_size) if use_size else 1)]
        # extract filename
        filename = ')'.join('('.join(' '.join(line[1:len(line) - 1]).split("(")[1:]).split(")")[:-1])
        # return formated list
        return [hashname, filename, hashstr] + ([size] if size != None else [])

# ~ Extra ~

# print to stderr
def eprint(*args, **kwargs):
    """Prints to stderr usefull for warnings and error messages"""
    print(*args, file=os.sys.stderr, **kwargs)

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

# ~ Detection ~

# detect file format
def detect_format(hashstr, use_size=False):
    """Autodetect hash format, by checking the length and what it contains"""
    if len(hashstr.split(" ")) < 0:
        # not valid hash
        return None
    # first split string
    tmp = [l for l in hashstr.split(" ") if not l in ("", "=")]
    # get hash for sfv and N/A formats
    tmp_hash = tmp[1 + use_size].replace("\n", "")
    # set one for bsd
    tmp_hash_b = tmp_hash
    # and get correct hash from it if so
    if len([l for l in hashstr.split(" ") if l != ""]) > 3:
        tmp_hash_b = tmp[2].replace("\n", "")

    # if the second element in the list is a hash then return sfv
    if len(tmp_hash) % 4 == 0 and ishex(tmp_hash) and not ("(" in hashstr and ")" in hashstr):
        # simple file verification
        return "sfv"

    # if both ( and ) is in the string return bsd
    elif ("(" and ")" in hashstr) and len(hashstr.split(" ")) > 2 and len(tmp_hash_b) % 4 == 0 and ishex(tmp_hash_b):
        # bsd style
        return "bsd"

    # else None at All
    return "N/A"

# detect and prompt user if needed
def choose_hash(hash1, hashit):
    """
    Uses detect.decect to identify hashes with a high accuracy but when
    there if some issues it will take user input. CLI-only
    """
    # check for valid hash
    if hasattr(hashit, "name"):
        # get result from detect.detect
        tup = detect(hash1, generate_data_set(GLOBAL["HASH_STR"], __algorithms__, new))
        # but only use if not already choosen

        # not valid hash
        if tup is None:
            return None

        if tup.certain and not (hashit.name in tup.certain or tup.maybe) and not tup.maybe:
            hashit = new(tup.certain[0])

        elif tup.maybe:
            # for each element in maybe
            for c, h in enumerate(tup.certain + tup.maybe):
                eprint(h, "(" + str(c) + ")")
            # get input by e-printing questing
            eprint(GLOBAL["MESSAGES"]["MAYBE_M"], end=" ")
            # and getting input as an int
            c_index = int(input())
            # fix output
            eprint("\n", end="")

            # then use the input as an index
            if len(tup.maybe) - 1 >= c_index:
                # choose maybe
                hashit = new((tup.certain + tup.maybe)[c_index])

            else:
                # if it's out of index
                # raise IndexError
                raise IndexError(GLOBAL["ERRORS"]["IndexError"])
        else:
            # the current hash is probaly the rigth one
            pass

    else:
        # else do noting
        pass

    # return hasher
    return hashit

# ~ Hash-functions ~

# inits a new hash-class
def new(hashname, data=b''):
    """Custom hash-init function that returns the hashes
    depends on hashlib.new and GLOBAL["EXTRA"]. One of its'
    features is it's support for the python3 only shake-hash
    scheme were the default hash is shake_256 and the input is
    taken like this:
        shake_[amount of output]"""
    # if it's a plugin
    if hashname in GLOBAL["EXTRA"]:
        return GLOBAL["EXTRA"][hashname](data)

    # shake hash
    elif hashname[:5] == "shake" and os.sys.version_info[0] == 3:
        return shake(hashname, data)

    # hashlib algorithm
    elif hashname in hashlib.algorithms_available:
        return hashlib.new(hashname, data)

    # else raise value error
    else:
        raise ValueError(hashname + " " + GLOBAL["MESSAGES"]["HASH_NOT"])

# loads a hash class into EXTRA
def load(hashclass):
    """
    Add hashes to GLOBAL.EXTRA which is the dict that contains all the "extra"
    hash-functions such as Crc32, which allows external hashing algorithms to 
    be used as long as the have the same api as specified in docs/README.md

    returns True/False based on whether or not the data is loaded
    """
    if "update" and "hexdigest" and "digest" in hashclass.__dict__:
        hashname = hashclass().name
        GLOBAL["EXTRA"][hashname] = hashclass
        return True

    # else return false
    return False

# loads a list of hash classes
def load_all(list_of_hashclasses):
    """Just for it, a function that loads all plugins in a list"""
    for hc in list_of_hashclasses:
        if not load(hc):
            eprint(hc, GLOBAL["MESSAGES"]["LOAD_FAIL"])
            continue

# hashIter goes over an bytes string
# block for block and updates the hash while
# not having the intire file in memory

def hashIter(bytesiter, hasher, ashexstr=True):
    """Will hash the blockIter generator and return digest"""
    for block in bytesiter:
        hasher.update(block)

    return hasher.hexdigest() if ashexstr else hasher.digest()

# blockIter creates bytestring-blocked
# byte data for hashIter

def blockIter(afile, blocksize=65536):
    """Will create a generator for reading a file"""
    with afile:
        block = afile.read(blocksize)
        while block:
            yield block
            block = afile.read(blocksize)


# hashfile, the function used for all file hashing-operations
def hashFile(filename, hasher, memory_opt=False):
    """hashFile is a simple way to hash files using diffrent methods"""
    # use fixpath
    filename = fixpath(filename)
    # is memopt is true hashit like that
    if memory_opt:
        return hashIter(blockIter(open(filename, "rb")), hasher, True)
    
    # else don't use memory optimatation
    with open(filename, "rb") as file:
        chash = new(hasher.name, file.read()).hexdigest()
    # and return current hash
    return chash

# ~ Check ~

# check_ reads an file generate with hashit or md5sum (or sfv compatible files) and
# compares the results by re-hashing the files and prints if there is any changes

def check_(path, hashit, first_line, sfv=False, size=False, bsdtag=False):
    """Will read an file which have a SFV compatible checksum-file or a standard one and verify the files checksum
    by creating an generator which loops over another generator which parses/reads the file and then it will check
    if the hash and optionally the size of the files matches the current state of them. For more info on how this work
    see docs/index.md#technical.
    """
    # using generator to save proccessing power for parsing
    # sfv file not much but for the sake of it.

    # set default varaibles
    x_reader = None

    # the indexes are used to specify were a specific item is
    # in a list generated from the fileformat
    name_index = 0 # for BSDTag, where the hash is located
    hash_index = 0 # where is the hash in the list
    path_index = 0 # where is the path in the list
    size_index = 1 # where is the size in the list
    max_elem = 2 # how many items are there in the list
    file_format = None # which format are you using


    # auto detect checksum file format
    detectFormat = lambda s, e: detect_format(s, size) == e

    if sfv or detectFormat(first_line, "sfv"):
        x_reader = lambda: SFV(path, size).read()
        # set indexes
        hash_index = 1
        path_index = 0

        # reset other varibles
        sfv = True
        bsdtag = False
        file_format = "sfv"

    elif bsdtag or detectFormat(first_line, "bsd"):
        # create reader
        x_reader = lambda: BSD(path, size).read()
        # set indexes
        hash_index = 2
        path_index = 1
        max_elem = 3

        # and reset other variables
        sfv = False
        bsdtag = True

        # set file format
        file_format = "bsd"

    else:
        # create reader
        x_reader = lambda: reader(path)
        # set indexes
        hash_index = 0
        path_index = 1
        # set file format to None At All
        file_format = "N/A"

    # check if you should add file sizes to the output
    if size:
        # BSDTag bump's everything up by one
        if bsdtag:
            size_index = 3
            max_elem = 4

        # bump max_elem by one
        elif sfv:
            size_index = 2
            max_elem = 3
        else:
            # bump path index up by one
            path_index = 2
            size_index = 1
            max_elem = 3

    # go over filedata-generator
    for data in x_reader():
        # convert string to data
        if not sfv and not bsdtag:
            # if it is None At All (N/a) then parse it normally
            data = [s for s in data.replace("\n", "").replace("\0", "").split(" ") if s != '']

        if bsdtag:
            if data[name_index] in list(GLOBAL["EXTRA"].keys()) or data[name_index][:5] in ("sha3_", "shake") or data[name_index] in hashlib.algorithms_available:
                hashit = new(data[name_index])

        # check format
        if len(data) > max_elem:
            # if there is something wrong with the format yield the error message
            yield (GLOBAL["MESSAGES"]["WRONG_FORMAT"] + " {} '{}' ".format(GLOBAL["MESSAGES"]["CUR_FORM"], file_format))
            # and continue
            continue

        # get hash and filepath from data-list with predefined indexes
        last_hash, filename = data[hash_index], fixpath(data[path_index]) # fix filename
        # try to hash file again
        # and print correct results
        if os.path.exists(filename):
            # hash file again
            '''
            Using generator to check for file because there is a memory leak when using a generator to check for it,
            it shouldn't be a problem because it's usaully faster than the generator but is still consired "slow" 
            because it uses way more memory.
            '''
            # current_hash = hashFile(filename, hashit, True)
            current_hash = new(hashit.name, open(filename, "rb").read()).hexdigest()

            current_size = None
            last_size = None

            # result of size_check
            # default: True
            size_check = True
            # set hashcheck
            hash_check = str(last_hash) == str(current_hash)

            # if we shall check the size diffrence
            # get last and current size
            if size:
                last_size = data[size_index]
                current_size = os.stat(filename).st_size
                try:
                    size_check = int(last_size) == int(current_size)

                except ValueError:
                    # os returns wrong size format
                    size_check = True

            # yield results
            yield {"filename":filename, "last_hash":last_hash, "current_hash":current_hash, "last_size":last_size, "current_size":current_size, "size_check":size_check, "hash_check":hash_check}

        else:
            # else continue and yield error message if the file does not exist
            yield (filename + ": " + "{}, ".format(GLOBAL["MESSAGES"]["FAIL"]) + GLOBAL["MESSAGES"]["FILE_NOT"])

def check(path, hashit, usecolors=False, be_quiet=False, detecthash=True, sfv=False, size=False, bsdtag=False, strict=False, trace=False):
    """Uses check_() to print the error messages and statuses corrent (for CLI)
    they are seperated so that you can use the python api, if you so please.
    """
    # set "global" colors
    RED = ""
    GREEN = ""
    YELLOW = ""
    RESET = ""
    # check if system supports color
    # and check if the colors is enabled
    if supports_color() and usecolors:
        # if so override the vars with the colors
        RED = GLOBAL["COLORS"]["RED"]
        GREEN = GLOBAL["COLORS"]["GREEN"]
        YELLOW = GLOBAL["COLORS"]["YELLOW"]
        RESET = GLOBAL["COLORS"]["RESET"]

    # check if file exits
    if not os.path.exists(path):
        eprint(RED + GLOBAL["MESSAGES"]["FILE_NOT"] + RESET)
        return 1

    # get first line from the file
    first_line = next(reader(path, "r"))

    # choose hash if not already selected
    # using new detection algorithem
    try:
        if detecthash:
            hash1 = first_line
            file_format = detect_format(first_line)
            # parse string and get hash
            if file_format == "sfv":
                hash1 = SFV.parser(first_line, size)[1]

            elif file_format == "bsd":
                hash1 = BSD.parser(first_line, size)[2]

            else:
                hash1 = [x for x in first_line.strip().replace("\n", "").split(" ") if x != ''][0]
            # get new hasher
            hashit = choose_hash(hash1, hashit)
            # check if it is empty
            if hashit is None:
                # if it is print error message
                eprint(YELLOW + GLOBAL["MESSAGES"]["WRONG_FORMAT"] + " {} '{}' ".format(GLOBAL["MESSAGES"]["CUR_FORM"], file_format) + RESET)
                # and return
                return 1

    # if indexerror
    except IndexError as error:
        # if no data in file
        if not first_line:
            eprint(RED + GLOBAL["MESSAGES"]["EMPTY_CHK"] + RESET)

        if not be_quiet:
            eprint(YELLOW + str(error) + RESET)

        if trace:
            raise error
        # if strict return 1
        if strict:
            return 1
        
        # Else return exit code 0
        return 0

    for c in check_(path, hashit, first_line, sfv, size, bsdtag):
        if not isinstance(c, dict):
            # if return value is string then it's a error
            # so print it

            if not be_quiet and not strict:
                eprint(YELLOW + str(c) + RESET)

            # if strict return 1
            if strict:
                eprint(RED + str(c) + RESET)
                return 1
            # and continue
            continue

        # check if there are any changes in the results end
        # from them that in the file
        # check_ does automaticly check if the values are equal

        if not c["hash_check"] or not c["size_check"]:
            # if the file has changed print notice (md5sum inpired)
            if not c["size_check"]:
                # change with file increase/decrease
                print(c["filename"] + ":" + GREEN, c["last_hash"] + RESET, ">", RED + c["current_hash"] + RESET, YELLOW + str(c["last_size"]) + RESET + "->" + YELLOW + str(c["current_size"]), end=RESET + '\n')
            else:
                # change in hash
                print(c["filename"] + ":" + GREEN, c["last_hash"] + RESET, ">", RED + c["current_hash"], end=RESET + '\n')

        # if not to be quiet
        elif not be_quiet:
            # print OK
            # else print OK if not quiet
            print(c["filename"] + ":" + GREEN, GLOBAL["MESSAGES"]["OK"], end=RESET + '\n')

    # return exit code
    return 0
