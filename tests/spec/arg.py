import argparse

__version__ = "3.3.3a0"

class Print(argparse.Action):
    def __init__(self, nargs=0, **kwargs):
        if nargs != 0:
            raise ValueError('nargs for StartAction must be 0; it is just a flag.')
        elif "text" in kwargs:
            self.data = kwargs.pop("text")

        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.data)

class Execute(argparse.Action):
    def __init__(self, nargs=0, **kwargs):
        if nargs != 0:
            raise ValueError('nargs for StartAction must be 0; it is just a flag.')
        
        if "func" in kwargs:
            self.data = kwargs.pop("func")

        if "exit" in kwargs:
            self.exit = True if kwargs.pop("exit") else False

        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.data())
        if self.exit:
            exit()

parser = argparse.ArgumentParser("hashit", "hashit [options] $path", "hashit is an hashing application...", "MIT License, Copyrigth (c) 2020 Javad Shafique")
parser.add_argument("-V", "--version", help="Print current version and exit", action="version", version="%(prog)s " + __version__)
parser.add_argument("-l", "--license", help="Print license and exit", action=Print, text="MIT")
parser.add_argument("-H", "--hash", help="Select hash use -hl --hash-list for more info")
parser.add_argument("-hl", "--hash-list", help="Prints list of all supported hashes and exits", action=Execute, func=lambda: 1, exit=True)
parser.add_argument("-a", "--all", help="Calculate all hashes for a single file")
parser.add_argument("-sfv", "--sfv", help="Outputs in a sfv compatible format", action="store_true")
parser.add_argument("-C", "--color", help="Enable colored output where it is supported", action="store_true")
parser.add_argument("-f", "--file", help="Hash single a file")
parser.add_argument("-S", "--size", help="Adds the file size to the output", action="store_true")
parser.add_argument("-s", "--string", help="hash a string or a piece of text", action="store_const", const=True)
parser.add_argument("-sp", "--strip-path", help="Strips fullpath from the results", action="store_true")
parser.add_argument("-A", "--append", help="Instead of writing to a file you will append to it", action="store_true")
parser.add_argument("-d", "--detect", help="Enable hash detection for check (can take argument)", action="store_const", const=True)
parser.add_argument("-m", "--memory-optimatation", help="Enables memory optimatation (useful for large files)", action="store_true")
parser.add_argument("-c", "--check", help="Verify checksums from a checksum file")
parser.add_argument("-q", "--quiet", help="Reduces output", action="store_true")
parser.add_argument("-bsd", "--bsd", help="output using the bsd checksum-format", action="store_true")
parser.add_argument("-o", "--output", help="output output to an output (file)")

args = parser.parse_args()
print(args)