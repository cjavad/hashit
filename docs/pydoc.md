<script>var link = "https://raw.githubusercontent.com/JavadSM/hashit/master/docs/favicon.ico"; var obj = document.createElement("link"); obj.rel = "shortcut icon"; obj.type="image/x-icon"; obj.href = link; document.getElementsByTagName("head")[0].append(obj);</script>

<h1 id="hashit">hashit</h1>

hashit module for hashit command is contaning all the code for hashit

hashit is an hashing application which main purpose is to replace all the 'default'
hashing commands that comes with linux and also provide a usable hashing program
for windows hence the choice of using python. while hashit supports both python 2 and 3
i would strongly recommend using python3 because that python3 comes with a newer version
of hashlib and therefore many new hash-functions, altough it is posible to add these into
python2 with the load() function which acts like a 'connecter' and enables hashit to use
third-party hashing-functions as long as the have the same api as specified in docs/README.md

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

<h2 id="hashit.fixpath">fixpath</h2>

```python
fixpath(path)
```
Returns full path and supports snap
<h2 id="hashit.eprint">eprint</h2>

```python
eprint(*args, **kwargs)
```
Prints to stderr usefull for warnings and error messages
<h2 id="hashit.supports_color">supports_color</h2>

```python
supports_color()
```

Returns True if the running system's terminal supports color, and False
otherwise.

<h2 id="hashit.detect_format">detect_format</h2>

```python
detect_format(s)
```
Autodetect hash format, by checking the length and what it contains
<h2 id="hashit.choose_hash">choose_hash</h2>

```python
choose_hash(hash1, hashit)
```

Uses detect.decect to identify hashes with a high accuracy but when
there if some issues it will take user input.

<h2 id="hashit.reader">reader</h2>

```python
reader(filename, mode='r', remove_binary_mark=True)
```
Creates generator for an file, better for larger files not part of the MEMOPT
<h2 id="hashit.read_sfv">read_sfv</h2>

```python
read_sfv(filename)
```
Creates generator that reads and parses sfv compatible files using reader
<h2 id="hashit.sfv_max">sfv_max</h2>

```python
sfv_max(file_hash, file_path, longest, size='')
```
calculates the amount of spaces needed in a sfv file
<h2 id="hashit.bsd_tag">bsd_tag</h2>

```python
bsd_tag(file_hash, file_path, hashname)
```
Formats string in a bsd style format
<h2 id="hashit.bsd2str">bsd2str</h2>

```python
bsd2str(bsdstr, size=False)
```
Parses a bsd compatible string to an array
<h2 id="hashit.new">new</h2>

```python
new(hashname, data=b'')
```
Custom hash-init function that returns the hashes
<h2 id="hashit.load">load</h2>

```python
load(hashclass)
```

Add hashes to GLOBAL.EXTRA which is the dict that contains all the "extra"
hash-functions such as Crc32, which allows external hashing algorithms to
be used as long as the have the same api as specified in docs/README.md

returns True/False based on whether or not the data is loaded

<h2 id="hashit.load_all">load_all</h2>

```python
load_all(list_of_hashclasses)
```
Just for it, a function that loads all plugins in a list
<h2 id="hashit.hashIter">hashIter</h2>

```python
hashIter(bytesiter, hasher, ashexstr=True)
```
Will hash the blockIter generator and return digest
<h2 id="hashit.blockIter">blockIter</h2>

```python
blockIter(afile, blocksize=65536)
```
Will create a generator for reading a file
<h2 id="hashit.hashFile">hashFile</h2>

```python
hashFile(filename, hasher, memory_opt=False)
```
hashFile is a simple way to hash files using diffrent methods
<h2 id="hashit.check">check</h2>

```python
check(path, hashit, useColors=False, be_quiet=False, detectHash=True, sfv=False, size=False, bsdtag=False)
```
Will read an file which have a SFV compatible checksum-file or a standard one and verify the files checksum
<h1 id="hashit.__main__">hashit.__main__</h1>

Command line program for hashit

this module "__main__" contains all the code for argparsing, running
and anything needed for an command lin application such as hashit.

it uses argc another package by me, but i am considering switching to argparse

<h2 id="hashit.__main__.Print">Print</h2>

```python
Print(self, nargs=0, **kwargs)
```
Print action for argparse, takes one kwarg which is text the varible which contains the string to be printed
<h2 id="hashit.__main__.Execute">Execute</h2>

```python
Execute(self, nargs=0, **kwargs)
```
Same as Print() but instead of printing an object it calls it takes func (function), and exit (bool)
<h2 id="hashit.__main__.walk">walk</h2>

```python
walk(go_over)
```
Goes over a path an finds all files, appends them to a list and returns that list
<h2 id="hashit.__main__.config">config</h2>

```python
config(parser)
```
Sets argvs' config and commands with argparse and returns it for good sake
<h2 id="hashit.__main__.main_">main_</h2>

```python
main_(args)
```
Main function which is the cli parses arguments and runs appropriate commands
<h2 id="hashit.__main__.main">main</h2>

```python
main(args=None)
```

Main function with error catching, can force-exit with os._exit(1)

this main function calls main_() and cathes any error while giving the user some "pretty"
errors.

<h1 id="hashit.detection">hashit.detection</h1>


Copyrigth (c) 2018-present Javad Shafique

this module using length and connections to find a match
for an hashing algorithem. It's basicly a matching algorigtem
it can be used for almost any pure function in this case for hashes.

__Copyright (c) 2018-present Javad Shafique__

__This 'Software' can't be used without permission__

__from Javad Shafique.__


__this module using length and connections to find a match__

__for an hashing algorithem. It's basicly a matching algorigtem__

__it can be used for almost any pure function in this case for hashes.__

__basic template:__



def generate_some_dataset(datatoworkon = "some data"):
    dict_for_storing_set = dict()

    for each_element in a_list_of_something_to_compare_with:
        data = function_that_uses_data_to_generate_something(each_element, datatoworkon)

        dict_for_storing_set.update({each_element:{"data":data, "size":len(data), "size-as":list(), "connection":list()}})


    `find` connection and size

    for each_element in dict_for_storing_set:
        elements_data = dict_for_storing_set[each_element]["data"]
        elements_size = dict_for_storing_set[each_element]["size"]

        for second_element in dict_for_storing_set:
            if dict_for_storing_set[second_element]["size"] == elements_size:
                if elements_data == dict_for_storing_set["data"]:
                    dict_for_storing_set[each_element]["connection"].append(second_element)
                else:
                    dict_for_storing_set[each_element]["size-as"].append(second_element)
            else:
                continue

    # return finished dataset

    return dict_for_storing_set

__and for parsing that infomation__

__you can use the detect function__

__as here:__



def detect(string, table, maybe = True):
    if not (type(string) == str):
        return None

    so = list()
    so_far = list()
    length = len(string)

    for key in table:
        dat = table[key]

        if dat["size"] == length:
            for i in dat["connection"]:
                if i not in so_far:
                    so_far.append(i)

    for i in so_far:
        dat = table[i]["connection"]

        for j in so_far:
            if not j in dat:
                so_far.remove(j)

    if maybe:
        for key in table:
            dat = table[key]

            if dat["size"] == length:
                so.append(key)

    if len(so_far) >= 0 and len(so) == 1:

        # if there only is one option then use it

        return tup(certain=so, maybe=[])
    else:
        return tup(certain=so_far, maybe=so)



__compare hashes for hash-detection__

__it can generate data that can compare__

__diffrences between the results__


__if works by categorizing the hashes into__

__two categorizes. one for thoose who look alike__

__and one for thoose who generates the same output__

__given the same input. And with it a sorted result__

__is outputted and is ready to be used be the user.__


__list of which algorithms is most likly used (WIP)__


PRIORITY = {
    "md5":["md5"],
    "sha1":["dsaEncryption", "DSA", "ecdsa-with-SHA1", "dsaWithSHA", "DSA-SHA"]
}

<h2 id="hashit.detection.ishex">ishex</h2>

```python
ishex(hexstr)
```
Checks if string is hexidecimal
<h2 id="hashit.detection.generate_data_set">generate_data_set</h2>

```python
generate_data_set(hashon, algos, hasher_that_takes_new)
```
Generates dataset based on data and list of strings that can be used to create objects to use that data
<h2 id="hashit.detection.NTUPLE">Closest</h2>

```python
Closest(self, /, *args, **kwargs)
```
Closest(certain, maybe)
<h2 id="hashit.detection.detect">detect</h2>

```python
detect(s, table, maybe=True)
```
Compares result from datasets, finds connections and eleminates contestants
<h1 id="hashit.extra">hashit.extra</h1>

Extra functions and classes for hashit
<h2 id="hashit.extra.Crc32">Crc32</h2>

```python
Crc32(self, data=b'')
```
This class is an api for the crc32 function that is compatible with mor
<h2 id="hashit.extra.shake">shake</h2>

```python
shake(self, hashname, data=b'')
```
Top-level api for hashlib.shake


[back](README.md)