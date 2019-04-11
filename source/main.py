"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

import sys
from antlr4 import *
from source.gen.CLexer import CLexer
from source.gen.CParser import CParser
from source.CListenerExtend import CListenerExtend


def main(argv):
    input_stream = FileStream("C_Files/simple_statements.cc")
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.statements()
    listener = CListenerExtend()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


if __name__ == '__main__':
    main(sys.argv)
