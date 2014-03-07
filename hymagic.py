#Notes use ip.register_magic_function to register the magic
#Make a magic class that has the functions
# see
# https://github.com/ipython/ipython/blob/master/IPython/extensions/storemagic.py
# Follow the example on runsource in
# https://github.com/hylang/hy/blob/master/hy/cmdline.py#L61
# Try putting print statements in for the returns?
# Use ip.run_ast_nodes with compiler=ast_compiler on the compiles hy _ast
import argparse
import code
import ast
import sys

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
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(HylangMagics)
