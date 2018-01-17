"""hashit module for hashit command is contaning all the code for hashit


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
from .detect import detect, generate_data_set

__author__ = "Javad Shafique" # copyrigth holder
__license__ = "MIT, Copyrigth (c) 2017-present Javad Shafique" # license foro program

# help message
# this list is the message that will be printed
# when the user uses hashit --help

# fix algo list by sorting it trough
__algorithems__ = sorted([s for s in hashlib.algorithms_available if not (s[:5] in ("shake") or \
        s[:3] in {"SHA", "MD5", "MD4", "RIP"})] + ["crc32"], key=len) # add crc32

__help__ = lambda help_command: ["Usage:\n", "   hashit [options] $path", "", help_command, "", \
     "Notice: this program was made by Javad Shafique, and uses argc another package by me\n"]

# Global config
CONFIG = {
    "raise":True,
    "FILE_NOT":"File does not exist",
    "COLORS":{
        "RED":"\x1b[0;31m",
        "GREEN":"\x1b[0;32m",
        "YELLOW":"\x1b[0;33m",
        "RESET":"\x1b[0m"
    },
    "USE_COLORS_DEFAULT":False
}

# exit alias for os.sys.exit
Exit = os.sys.exit

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


def choose_hash(hash1, hashit):
    """
    Uses detect.decect to identify hashes with a high accuracy but when
    there if some issues it will take user input.
    """
    # check for valid hash
    if hasattr(hashit, "name"):
        # get result from detect.detect
        tup = detect(hash1, generate_data_set("Hallo", __algorithems__, new))
        # but only use if not already choosen

        # not valid hash
        if tup is None:
            return None

        if len(tup.certain) >= 1 and not (hashit.name in tup.certain or hashit.name in tup.maybe):
            hashit = new(tup.certain[0])
        
        elif len(tup.maybe) >= 1:
            # for each element in maybe
            for c, h in enumerate(tup.maybe):
                eprint(h, "(" + str(c) + ")")
            # get input by printing questing
            eprint("Did you maybe mean:", end=" ")
            # and getting input as an int
            c_index = int(input())
            # fix output
            eprint("\n", end="")

            # then use the input as an index
            if len(tup.maybe) - 1 >= c_index:  
                # choose maybe
                hashit = new(tup.maybe[c_index])

            else:
                # if it's out of index
                # raise IndexError
                raise IndexError

        else:
            # choose anyone from certain
            # as they will all work
            eprint("Using", tup.certain[0])

    else:
        # else do noting
        pass

    return hashit

def reader(filename, mode="r", remove_binary_mark=True):
    """Creates generator for file"""
    return (line.replace("*", "") if remove_binary_mark else line for line in open(filename, mode=mode).readlines())

# read sfv file and create and generator with correct results
def read_sfv(filename):
    """Creates generator that reads and parses sfv compatible files"""
    # remove spaces from string
    return (' '.join([l for l in l.split(" ") if l != '']) for l in reader(filename, "r"))

# calculates the amount of spaces needed in a sfv file
def sfv_max(file_hash, file_path, longest, size=""):
    """calculates the amount of spaces needed in a sfv file"""
    if len(size) > 0:
        size = " " + size 

    spaces = " "
    if len(file_path) - 1 < longest:
        spaces = spaces*(longest - len(file_path) + 1)
    # return sfv compatible string
    return file_path + spaces + (file_hash + size)

# creates new hash
def new(hashname, data=b''):
    if hashname == "crc32":
        return Crc32(data)
    elif hashname[:5] == "shake" and os.sys.version_info[0] == 3:
        return shake(hashname, data)

    elif hashname in hashlib.algorithms_available:
        return hashlib.new(hashname, data)
    
    else:
        raise ValueError(hashname + " is not a valid hash type")


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
    """Will create generator for reading file"""
    with afile:
        block = afile.read(blocksize)
        while block:
            yield block
            block = afile.read(blocksize)

# do not use, at least 10 times slower than any other method
def easy_hash(filename, hasher):
    """Slow but easy to use self-contained hasher"""
    # openfile
    with open(filename, "rb") as afile: 
        for block in (line for line in afile.readlines()):
            hasher.update(block)
    # return hash
    return hasher.hexdigest()

# hashfile, the function used for all file hashing-operations
def hashFile(filename, hasher, memory_opt=False):
    """hashFile is a simple way to hash files using """
    if memory_opt:
        return hashIter(blockIter(open(filename, "rb")), hasher, True)
    else:
        # dont use memory optimatation but close file
        with open(filename, "rb") as file:
            hash = new(hasher.name, file.read()).hexdigest()
        return hash

# check reads an file generate with hashit or md5sum (or sfv compatible files) and
# compares the results by re-hashing the files and prints if there is any changes

def check(path, hashit, useColors=False,  be_quiet=False, detectHash=True, sfv=False, size=False):
    """Will read an file which have a SFV compatible checksum-file or a standard one and verify the files checksum"""

    # set colors
    RED = CONFIG["COLORS"]["RED"]
    GREEN = CONFIG["COLORS"]["GREEN"]
    YELLOW = CONFIG["COLORS"]["YELLOW"]
    RESET = CONFIG["COLORS"]["RESET"]

    # check if system supports color
    # with bitwise-exclusive or (XOR)
    if supports_color() ^ useColors:
        # if not override values
        RED = ""
        GREEN = ""
        YELLOW = ""
        RESET = ""

    hash_index = int()
    path_index = int()
    
    # check if file exits
    if not os.path.exists(path):
        eprint(RED + CONFIG["FILE_NOT"] + RESET)
        return

    # using generator to save proccessing power for parsing
    # sfv file not much but for the sake of it.

    # set default varaibles
    x_reader = None
    hash_index = 0
    path_index = 0
    size_index = 1

    max_elem = 2


    if sfv:
        x_reader = lambda: read_sfv(path)
        # get length of file
        length = sum(1 for i in x_reader())
        # set indexes
        hash_index = 1
        path_index = 0
    else:
        x_reader = lambda: reader(path)
        length = sum(1 for i in x_reader())
        # set indexes
        hash_index = 0
        path_index = 1

    # check if you should add file sizes to the output
    if size:
        max_elem = 3    
        size_index = 1

        if sfv:
            size_index = 2
        else:
            path_index = 2

    # choose hash if not already selected
    # using new detection algorithem
    try:
        if detectHash:
            # get first line from the file
            first_line = open(path, "r").readline()
            # get hash from line
            hash1 = [x for x in first_line.replace("\n", "").replace("\0", "").split(" ") if x != ''][hash_index]
            # get new hasher
            hashit = choose_hash(hash1, hashit)

            if hashit == None:
                eprint(YELLOW + "Checksum-file does not seem to be valid, maybe it is a sfv file? (try -sfv)" + RESET)
                return

    except IndexError:
        # if no data in file
        if length <= 0:
            eprint(RED + "checksum file is empty" + RESET)
            return

    # go over filedata-generator
    for line in x_reader():
        # convert string to data
        data = [s for s in line.replace("\n", "").replace("\0", "").split(" ") if s != '']

        if len(data) != max_elem:
            # then there is something wrong with the format
            continue
        
        # get hash and filepath from data-list with predefined indexes
        last_hash, filename = data[hash_index], data[path_index]
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

            current_size = int()
            last_size = int()

            SizeCheck = True

            if size:
                last_size = data[size_index]
                current_size = os.stat(filename).st_size
                SizeCheck = int(last_size) == int(current_size)

            if not current_hash == last_hash or not SizeCheck:
                # if the file has changed print notice (md5sum inpired)
                if not SizeCheck:
                    print(filename + ":" + GREEN, last_hash + RESET, ">", RED + current_hash + RESET, YELLOW + str(last_size) + RESET + "->" + YELLOW + str(current_size) , end=RESET + '\n')
                else: 
                    print(filename + ":" + GREEN, last_hash + RESET, ">", RED + current_hash, end=RESET + '\n')

            elif not be_quiet:
                # else print OK if not quiet
                print(filename + ":" + GREEN, "OK", end=RESET + '\n')


        elif not be_quiet:
            # file does not exist
            eprint(RED + filename + ":", "FAILED, File does not exist" + RESET)
            # and continue
            continue

        else:
            continue
