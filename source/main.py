"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
import subprocess
import sys
from antlr4 import *

from source.gen.CLexer import CLexer
from source.gen.CParser import CParser
import source.CListenerExtend as CListenerExtend


def main(argv):
    input_file = "C_Files/simple_statements.cc"
    input_stream = FileStream(input_file)
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.statements()
    listener = CListenerExtend.CListenerExtend(input_file)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    ast = listener.ast
    dot_file = "AST.dot"
    ast.to_dot(dot_file)
    subprocess.call(["dot", "-Tpng", dot_file, "-o", "AST.png"])
    if ast.failed:
        print("I failed :(")

    else:
        print(ast.generate_llvm())

if __name__ == '__main__':
    main(sys.argv)
