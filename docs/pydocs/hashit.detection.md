  ------------------------------------- -----------------------------------------------------------------------------------------------------------------------------
   \                                    [index](.)\
   \                                    [/home/javad/Dropbox/playground/hashit/hashit/detection.py](file:/home/javad/Dropbox/playground/hashit/hashit/detection.py)
  **[hashit](hashit.html).detection**   
  ------------------------------------- -----------------------------------------------------------------------------------------------------------------------------

`Copyrigth (c) 2018-present Javad Shafique   this module using length and connections to find a match  for an hashing algorithem. It's basicly a matching algorigtem it can be used for almost any pure function in this case for hashes.   # Copyright (c) 2018-present Javad Shafique # This 'Software' can't be used without permission # from Javad Shafique.   # this module using length and connections to find a match  # for an hashing algorithem. It's basicly a matching algorigtem # it can be used for almost any pure function in this case for hashes. # basic template:     def generate_some_dataset(datatoworkon = "some data"):     dict_for_storing_set = dict()       for each_element in a_list_of_something_to_compare_with:         data = function_that_uses_data_to_generate_something(each_element, datatoworkon)           dict_for_storing_set.update({each_element:{"data":data, "size":len(data), "size-as":list(), "connection":list()}})         #find connection and size          for each_element in dict_for_storing_set:         elements_data = dict_for_storing_set[each_element]["data"]         elements_size = dict_for_storing_set[each_element]["size"]           for second_element in dict_for_storing_set:             if dict_for_storing_set[second_element]["size"] == elements_size:                 if elements_data == dict_for_storing_set["data"]:                     dict_for_storing_set[each_element]["connection"].append(second_element)                 else:                     dict_for_storing_set[each_element]["size-as"].append(second_element)             else:                 continue       # return finished dataset          return dict_for_storing_set   # and for parsing that infomation  # you can use the detect function # as here:     def detect(string, table, maybe = True):     if not (type(string) == str):         return None          so = list()     so_far = list()     length = len(string)          for key in table:         dat = table[key]           if dat["size"] == length:             for i in dat["connection"]:                 if i not in so_far:                     so_far.append(i)          for i in so_far:         dat = table[i]["connection"]           for j in so_far:             if not j in dat:                 so_far.remove(j)       if maybe:         for key in table:             dat = table[key]               if dat["size"] == length:                 so.append(key)       if len(so_far) >= 0 and len(so) == 1:               # if there only is one option then use it               return tup(certain=so, maybe=[])     else:         return tup(certain=so_far, maybe=so)       # compare hashes for hash-detection # it can generate data that can compare # diffrences between the results   # if works by categorizing the hashes into  # two categorizes. one for thoose who look alike # and one for thoose who generates the same output # given the same input. And with it a sorted result # is outputted and is ready to be used be the user.   # list of which algorithms is most likly used (WIP)   PRIORITY = {     "md5":["md5"],     "sha1":["dsaEncryption", "DSA", "ecdsa-with-SHA1", "dsaWithSHA", "DSA-SHA"] }`

 \
**Modules**

`      `

 

  ------------------------ -- -- --
  [string](string.html)\         
  ------------------------ -- -- --

 \
**Classes**

`      `

 

[builtins.tuple](builtins.html#tuple)([builtins.object](builtins.html#object))

Closest

 \
**NTUPLE** = [class
Closest]{#NTUPLE}([builtins.tuple](builtins.html#tuple))

`   `

`Closest(certain, maybe) `

 

Method resolution order:
:   Closest
:   [builtins.tuple](builtins.html#tuple)
:   [builtins.object](builtins.html#object)

------------------------------------------------------------------------

Methods defined here:\

[**\_\_getnewargs\_\_**]{#Closest-__getnewargs__}(self)
:   `Return self as a plain tuple.  Used by copy and pickle.`

<!-- -->

[**\_\_repr\_\_**]{#Closest-__repr__}(self)
:   `Return a nicely formatted representation string`

<!-- -->

[**\_asdict**]{#Closest-_asdict}(self)
:   `Return a new OrderedDict which maps field names to their values.`

<!-- -->

[**\_replace**]{#Closest-_replace}(\_self, \*\*kwds)
:   `Return a new Closest object replacing specified fields with new values`

------------------------------------------------------------------------

Class methods defined here:\

[**\_make**]{#Closest-_make}(iterable, new=&lt;built-in method \_\_new\_\_ of type object at 0x9e2040&gt;, len=&lt;built-in function len&gt;) from [builtins.type](builtins.html#type)
:   `Make a new Closest object from a sequence or iterable`

------------------------------------------------------------------------

Static methods defined here:\

[**\_\_new\_\_**]{#Closest-__new__}(\_cls, certain, maybe)
:   `Create new instance of Closest(certain, maybe)`

------------------------------------------------------------------------

Data descriptors defined here:\

**certain**
:   `Alias for field number 0`

<!-- -->

**maybe**
:   `Alias for field number 1`

------------------------------------------------------------------------

Data and other attributes defined here:\

**\_fields** = ('certain', 'maybe')

**\_source** = "from builtins import property as \_property,
tupl...\_itemgetter(1), doc='Alias for field number 1')\\n\\n"

------------------------------------------------------------------------

Methods inherited from [builtins.tuple](builtins.html#tuple):\

[**\_\_add\_\_**]{#Closest-__add__}(self, value, /)
:   `Return self+value.`

<!-- -->

[**\_\_contains\_\_**]{#Closest-__contains__}(self, key, /)
:   `Return key in self.`

<!-- -->

[**\_\_eq\_\_**]{#Closest-__eq__}(self, value, /)
:   `Return self==value.`

<!-- -->

[**\_\_ge\_\_**]{#Closest-__ge__}(self, value, /)
:   `Return self>=value.`

<!-- -->

[**\_\_getattribute\_\_**]{#Closest-__getattribute__}(self, name, /)
:   `Return getattr(self, name).`

<!-- -->

[**\_\_getitem\_\_**]{#Closest-__getitem__}(self, key, /)
:   `Return self[key].`

<!-- -->

[**\_\_gt\_\_**]{#Closest-__gt__}(self, value, /)
:   `Return self>value.`

<!-- -->

[**\_\_hash\_\_**]{#Closest-__hash__}(self, /)
:   `Return hash(self).`

<!-- -->

[**\_\_iter\_\_**]{#Closest-__iter__}(self, /)
:   `Implement iter(self).`

<!-- -->

[**\_\_le\_\_**]{#Closest-__le__}(self, value, /)
:   `Return self<=value.`

<!-- -->

[**\_\_len\_\_**]{#Closest-__len__}(self, /)
:   `Return len(self).`

<!-- -->

[**\_\_lt\_\_**]{#Closest-__lt__}(self, value, /)
:   `Return self<value.`

<!-- -->

[**\_\_mul\_\_**]{#Closest-__mul__}(self, value, /)
:   `Return self*value.n`

<!-- -->

[**\_\_ne\_\_**]{#Closest-__ne__}(self, value, /)
:   `Return self!=value.`

<!-- -->

[**\_\_rmul\_\_**]{#Closest-__rmul__}(self, value, /)
:   `Return self*value.`

<!-- -->

[**count**]{#Closest-count}(...)
:   `T.count(value) -> integer -- return number of occurrences of value`

<!-- -->

[**index**]{#Closest-index}(...)
:   `T.index(value, [start, [stop]]) -> integer -- return first index of value. Raises ValueError if the value is not present.`

 \
**Functions**

`      `

 

[**detect**]{#-detect}(s, table, maybe=True)
:   `Compares result from datasets, finds connections and eleminates contestants`

<!-- -->

[**generate\_data\_set**]{#-generate_data_set}(hashon, algos, hasher\_that\_takes\_new)
:   `Generates dataset based on data and list of strings that can be used to create objects to use that data`

<!-- -->

[**ishex**]{#-ishex}(hexstr)
:   `Checks if string is hexidecimal`

