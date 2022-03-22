---
title: Pandas Indexing Basics 
tags: data pandas python
---

What's the difference between .loc, .iloc, and .ix?

<!-- more -->

## Data access attributes
The primary means of doing Series/DataFrame selection (read: data access) are
the attributes `loc`, `iloc`, and `ix`. All of these provide dictionary-style
access to the items in a `Series` or rows in a `DataFrame`. It's not easy to
deduce from their names how these attributes differ from each other though, so
let's take a closer look at each.

### loc
According to the pandas documentation this is a "Purely label-location based
indexer for selection by label". Basically, **use `loc` for indexes with
meaningul label values**. In this example our index labels are strings:
```python
In [1]: import numpy as np

In [2]: import pandas as pd

In [3]: s = pd.Series([1, 2, 3], pd.Index(["whitefish", "perch", "trout"]))

In [4]: s.loc["perch"]
Out[4]: 2
```
A more common scenario however is to import data with a date column that we want
to use as the index. Below we'll manually construct a `Series` whose index is a
bunch of strings that we want to parse as dates. So we'll first use the
`pandas.to_datetime` function to convert these to dates in a fast, vectorized
way, and then we can use the `loc` attribute to look up items in the series by
date:
```python
In [5]: import datetime

In [6]: s = pd.Series([1, 2, 3], pd.Index(["2016-01-01", "2016-02-01", "2016-03-01"]))

In [7]: s.index
Out[7]: Index(['2016-01-01', '2016-02-01', '2016-03-01'], dtype='object')

In [8]: s.index = pd.to_datetime(s.index)

In [9]: s.loc[datetime.datetime(2016, 3, 1)]
Out[9]: 3
```
You can even do slices!
```python
In [10]: s.loc[datetime.datetime(2016, 2, 1):]
Out[10]: 
2016-02-01    2
2016-03-01    3
dtype: int64
```
Trying to access `s.loc[0]` throws a `TypeError` though, because there is no
element in the index whose value is 0. If we want to use position-based lookups,
we need to use a different attribute: `iloc`:

### iloc
`iloc` performs integer-based access to the index, purely by position: that is,
**if you think of the of the `Series` or `DataFrame` as a list of values or
rows, `iloc` does normal 0-based list access**.
```python
In [11]: s
Out[11]:
2016-01-01    1
2016-02-01    2
2016-03-01    3
dtype: int64

In [12]: s.iloc[0]
Out[12]: 1

In [13]: df = pd.DataFrame({"Superior": {"whitefish": 4, "perch": 0, "trout": 2},
                            "Erie":     {"whitefish": 0, "perch": 3, "trout": 1}})

In [14]: df
Out[14]:
           Erie  Superior
perch         3         0
trout         1         2
whitefish     0         4

In [15]: df.iloc[2]
Out[15]:
Erie        0
Superior    4
Name: whitefish, dtype: int64
```
`iloc` of course only accepts integers, although it'll happily accept negatives or slices:
```python
In [18]: df.iloc[-2]
Out[18]:
Erie        1
Superior    2
Name: trout, dtype: int64

In [19]: df.iloc[:-1]
Out[19]:
       Erie  Superior
perch     3         0
trout     1         2
``` 

### ix
`ix` supports both label (IE, index label value) and positional access: it looks
first for a label and falls back to positional access if no label with the given
value is found. It is a handy shortcut, especially if you want to do things like
access your index by label but your columns by position:
```python
In [20]: df = pd.DataFrame(np.random.randint(10, size=12).reshape(3,4),
                  index=['perch', 'trout', 'whitefish'],
                  columns=['male', 'female', 'adult', 'juvenile'])
Out[20]:
           male  female  adult  juvenile
perch         2       3      6         2
trout         0       3      1         4
whitefish     7       3      1         0

In [21]: df.ix['perch', 2:]
Out[21]:
adult       9
juvenile    8
Name: perch, dtype: int32
```
`ix` is safe to use for all cases except when your series or dataframe has a
"sparse" integer index -- IE an integer index where values may be missing. In
that case `ix` only does label-based selection and if the index does not contain
the desired value a `KeyError` will be raised. In this case, to avoid ambiguity,
either use `.loc` (if you explicitly want a `KeyError` in this case) or
`.iloc` (if you don't).

### Dictionary-style access
`Series` and `DataFrame` objects also support standard python dictionary style
access, which works exactly the same as `ix`:
```python
In [22]: s
Out[22]:
1    0
2    1
3    2
4    3
5    4
dtype: int32

In [23]: s[1]
Out[23]: 0

In [24]: s[0]
----------------------------
KeyError
```

### Summary

Here are the basic rules of thumb for data selection in pandas:

  - Use `.loc` if your index's labels are meaningful values.
  - Use `.iloc` if you want to treat your data like a list.
  - Use `.ix` or dictionary access for either, but beware of possible ambiguity
    and corner cases.