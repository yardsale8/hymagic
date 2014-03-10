"""
 Copyright (c) 2013 Paul Tagliamonte <paultag@debian.org>
 Copyright (c) 2013 Gergely Nagy <algernon@madhouse-project.org>
 Copyright (c) 2013 James King <james@agentultra.com>
 Copyright (c) 2013 Julien Danjou <julien@danjou.info>
 Copyright (c) 2013 Konrad Hinsen <konrad.hinsen@fastmail.net>
 Copyright (c) 2013 Thom Neale <twneale@gmail.com>
 Copyright (c) 2013 Will Kahn-Greene <willg@bluesock.org>
 Copyright (c) 2013 Bob Tolbert <bob@tolbert.org>

 Permission is hereby granted, free of charge, to any person obtaining a
 copy of this software and associated documentation files (the "Software"),
 to deal in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE SOFTWARE.

 hymagic is an adaptation of the HyRepl to allow ipython iteration
 hymagic author - Todd Iverson
 Available as github.com/yardsale8/hymagic
"""
import argparse
import code
import ast
import sys
import re

import hy

from hy.lex import LexException, PrematureEndOfInput, tokenize
from hy.compiler import hy_compile, HyTypeError
from hy.importer import ast_compile, import_buffer_to_module
from hy.completer import completion

from hy.macros import macro, require
from hy.models.expression import HyExpression
from hy.models.string import HyString
from hy.models.symbol import HySymbol

from hy._compat import builtins

SIMPLE_TRACEBACKS = True



from IPython.core.magic import Magics, magics_class, line_cell_magic


@magics_class
class HylangMagics(Magics):
    """Magic for the hylang lisp language
    """
    def __init__(self, shell):
        """
        Parameters
        ----------
        shell : IPython shell

        """
        super(HylangMagics, self).__init__(shell)
    @line_cell_magic
    def hylang(self, line, cell=None, filename='<input>', symbol='single'):
        """ Ipython magic function for running hylang code in ipython
        Use %hylang one line of code or
            %%hylang for a block or cell
            Note that we pass the AST directly to IPython."""
        global SIMPLE_TRACEBACKS
        source = cell if cell else line
        try:
            tokens = tokenize(source)
        except PrematureEndOfInput:
            print( "Premature End of Input" )
        except LexException as e:
            if e.source is None:
                e.source = source
                e.filename = filename
            print(str(e))
        try:
            _ast = hy_compile(tokens, "__console__", root=ast.Interactive)
            self.shell.run_ast_nodes(_ast.body,'<input>',compiler=ast_compile)
        except HyTypeError as e:
            if e.source is None:
                e.source = source
                e.filename = filename
            if SIMPLE_TRACEBACKS:
                print(str(e))
            else:
                self.shell.showtraceback()
        except Exception:
            self.shell.showtraceback()
    def hy(self, line, cell=None, filename='<input>', symbol='single'):
        ''' An short alias for the hylang magic
           Use %hy for a line of hylang code and %%hy for a block of code
        '''
        self.hylang(line, cell=None, filename='<input>', symbol='single')

#A regular expression for things that are clearly not hylang but python
notSexp = re.compile(r"""(?<! \( ) \s* ,  #Any comma not proceeded by paren
                         | : #no colons in hylang
                         | ^\s*[^[{(].*   #line doesnt start with delimiters
                         | .*[^]})]\s*$   #line doesn't end with delimiters
                         | (?<!\()\s* for #for preceeded by (
                         | (?<!\()\s*=   #equals not proceeded by ("""
                     , re.VERBOSE)

pcode = '''def adder(L):
    """a function to add lists"""
    tot = 0
    for val in L:
        tot += val
    return val
    a = [1, 2, 3]
    b = adder(L)
    c = [str(val) for val in a]
'''

def test_notSexp():
    '''test the notSexp on some python code'''
    assert all([bool(re.search(notSexp,l)) for l in pcode])
#TODO: Look at coroutine transformers for hacking ipython
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(HylangMagics)
