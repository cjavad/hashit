"""
Copyrigth (c) 2018-present Javad Shafique

this module using length and connections to find a match 
for an hashing algorithem. It's basicly a matching algorigtem
it can be used for almost any pure function in this case for hashes.

# Copyright (c) 2018-present Javad Shafique
# This 'Software' can't be used without permission
# from Javad Shafique.

# this module using length and connections to find a match 
# for an hashing algorithem. It's basicly a matching algorigtem
# it can be used for almost any pure function in this case for hashes.
# basic template:


def generate_some_dataset(datatoworkon = "some data"):
    dict_for_storing_set = dict()

    for each_element in a_list_of_something_to_compare_with:
        data = function_that_uses_data_to_generate_something(each_element, datatoworkon)

        dict_for_storing_set.update({each_element:{"data":data, "size":len(data), "size-as":list(), "connection":list()}})


    #find connection and size
    
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

# and for parsing that infomation 
# you can use the detect function
# as here:


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



# compare hashes for hash-detection
# it can generate data that can compare
# diffrences between the results

# if works by categorizing the hashes into 
# two categorizes. one for thoose who look alike
# and one for thoose who generates the same output
# given the same input. And with it a sorted result
# is outputted and is ready to be used be the user.

# list of which algorithms is most likly used (WIP)

PRIORITY = {
    "md5":["md5"],
    "sha1":["dsaEncryption", "DSA", "ecdsa-with-SHA1", "dsaWithSHA", "DSA-SHA"]
}
"""

import string
from collections import namedtuple

# checks if string is hex
def ishex(hexstr):
    """Checks if string is hexidecimal"""
    return all(char in string.hexdigits for char in hexstr)

def generate_data_set(hashon, algos, hasher_that_takes_new):
    """Generates dataset based on data and list of strings that can be used to create objects to use that data"""
    data_dict = dict()
    # go over the algorithms
    for algo in algos:
        hashed = hasher_that_takes_new(algo, hashon.encode()).hexdigest()
        # create dict in dict with all infomation stored in a table
        data_dict.update({algo:{"data":hashed, "size":len(hashed), "size-as":list(), "connection":list()}})

    for key in data_dict:
        # set default values
        hashed = data_dict[key]["data"]
        length = data_dict[key]["size"]

        for second in data_dict:
            if length == data_dict[second]["size"] and not second == key:
                if hashed == data_dict[second]["data"]:
                    data_dict[key]["connection"].append(second)
                else:
                    data_dict[key]["size-as"].append(second)
            else:
                continue
    
    return data_dict
        
# return value for detect, a named tuple with two values
NTUPLE = namedtuple("Closest", ["certain", "maybe"])


# detection function returns NTYPLE
def detect(s, table, maybe=True):
    """Compares result from datasets, finds connections and eleminates contestants"""
    if not (len(s) % 4 == 0 and ishex(s)):
        return None

    so = list()
    so_far = list()
    length = len(s)
  
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
        return NTUPLE(certain=so, maybe=[])
    else:
        return NTUPLE(certain=so_far, maybe=so)
