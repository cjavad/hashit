# Copyright (c) 2018-present Javad Shafique
# This 'Software' can't be used without permission
# from Javad Shafique.

from collections import namedtuple
import hashlib, json
from .__init__ import __algorithems__

# this module using length and connections to find a match 
# for an hashing algorithem. It's basicly a matching algorigtem
# it can be used for almost any pure function in this case for hashes.
# basic template:

"""
def generate_some_dataset(datatoworkon = "some data"):
    dict_for_storing_set = dict()

    for each_element in a_list_of_something_to_compare_with:
        data = function_that_uses_data_to_generate_something(each_element, datatoworkon)

        dict_for_storing_set.update({each_element:{"data":data, "size":len(data), "size-as":list(), "connection":list()}})


    #find connection and size
    
    for each_element in dict_for_storing_set.keys():
        elements_data = dict_for_storing_set[each_element]["data"]
        elements_size = dict_for_storing_set[each_element]["size"]

        for second_element in dict_for_storing_set.keys():
            if dict_for_storing_set[second_element]["size"] == elements_size:
                if elements_data == dict_for_storing_set["data"]:
                    dict_for_storing_set[each_element]["connection"].append(second_element)
                else:
                    dict_for_storing_set[each_element]["size-as"].append(second_element)
            else:
                continue
 
    # return finished dataset
    
    return dict_for_storing_set
"""

# and for parsing that infomation 
# you can use the detect function
# as here:

"""
def detect(string, table, maybe = True):
    if not (type(string) == str):
        return None
    
    so = list()
    so_far = list()
    length = len(string)
    
    for key in table.keys():
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
        for key in table.keys():
            dat = table[key]

            if dat["size"] == length:
                so.append(key)

    if len(so_far) >= 0 and len(so) == 1:
     
        # if there only is one option then use it
     
        return tup(certain=so, maybe=[])
    else:
        return tup(certain=so_far, maybe=so)

"""

# compare hashes for hash-detection
# for now has no method semmed vaiable
# it can generate data that can compare
# diffrences between the results

def generate_data_set(hashon = "Hello World!"):
    data_dict = dict()
    # go overt algorithems
    for algo in __algorithems__:
        hashed = hashlib.new(algo, hashon.encode()).hexdigest()
        # create dict in dict with all infomation stored in a table
        data_dict.update({algo:{"data":hashed, "len":len(hashed), "size-as":list(), "connection":list()}})

    for key in data_dict.keys():
        # set default values
        hashed = data_dict[key]["data"]
        length = data_dict[key]["len"]

        for second in data_dict.keys():
            if length == data_dict[second]["len"] and not second == key:
                if hashed == data_dict[second]["data"]:
                    data_dict[key]["connection"].append(second)
                else:
                    data_dict[key]["size-as"].append(second)
            else:
                continue
    
    return data_dict
        
# return value for detect
tup = namedtuple("Closest", ["certain", "maybe"])
# global dataset
data = generate_data_set()


def detect(string, table = data, maybe = True):
    if not (type(string) == str):
        return None
    
    so = list()
    so_far = list()
    length = len(string)
    
    for key in table.keys():
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
        for key in table.keys():
            dat = table[key]

            if dat["size"] == length:
                so.append(key)

    if len(so_far) >= 0 and len(so) == 1:
        # if there only is one option then use it
        return tup(certain=so, maybe=[])
    else:
        return tup(certain=so_far, maybe=so)

""" Usage:
hashdata = b"Hello World"

h = hashlib.new("md5", hashdata).hexdigest()

s = detect(h)
'''
for i in s:
    h1 = hashlib.new(i, hashdata).hexdigest()
    print(h1, h, h1 == h)
'''
print(s)
"""