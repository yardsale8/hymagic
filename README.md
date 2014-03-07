
## hymagic - A ipython extention for the hy LISP langauge
[Hylang](hylang.org), or simply hy, is a LISP language that is built on top of
the [Python programming language](python.org).

The `hymagic` ipython extension allows you to execute hylang code interactively
in a ipython console, qtconsole, or notebook.

### Installation

First, make sure that `hymagic.py` is in your python path, the suggested
location for ipython extensions is

In[6]:

```
from __future__ import print_function
import os
ip = get_ipython()
print(os.path.join(ip.ipython_dir, 'extensions'))
```


    /home/tiverson/.config/ipython/extensions


### Loading the `hymagic` extension

In[7]:

```
%load_ext hymagic
```

### Executing a hylang cell

You can execute a hylang cell using the `%%hylang magic` as shown below.

In[8]:

```
%%hylang
(defn add1 [n]
    (+ n 1))

(print (add1 5))
(add1 11)
```


    6




    12L



### Python interopt

Since hylang code is executed as python AST nodes in the regular ipython kernel,
you can freely intersperse hylang code and python code.

In[9]:

```
#Here we call the add1 function defined above in 
#regular python code
for i in range(4):
    print(add1(i))
```


    1
    2
    3
    4


### Execute a hylang line

You can also use the `%hylang` magic to execute one line of code

In[11]:

```
a = 5
%hylang (def a (add1 a)) 
a = a + 1
print(a)
```


    7


In[ ]:

```

```
