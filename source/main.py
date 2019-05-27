"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
import subprocess
import sys
from antlr4 import *

from gen.CLexer import CLexer
from gen.CParser import CParser
import CListenerExtend as CListenerExtend


def main(argv):
    # input_file = argv[0]
    input_file = "C_files/simple_statements.c"
    input_stream = FileStream(input_file)
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    if parser.getNumberOfSyntaxErrors() is not 0:
        return 1
    tree = parser.statements()
    listener = CListenerExtend.CListenerExtend(input_file)
    walker = ParseTreeWalker()

    walker.walk(listener, tree)

    ast = listener.ast

    dot_file = "AST.dot"
    if len(argv) == 3:
        dot_file = argv[2]
    ast.to_dot(dot_file)
    dot_name = dot_file[0: -4]
    dot_name += ".png"
    subprocess.call(["dot", "-Tpng", dot_file, "-o", dot_name])
    if ast.failed:
        print("Failed to compile.")

    else:
        # f = open(argv[1], 'w+')
        f = open("result.llsv", 'w+')
        # f.writelines(ast.generate_llvm())
        f.close()

    ast.first_pass()
    dot_file = "AST2.dot"
    ast.to_dot(dot_file)
    dot_name = dot_file[0: -4]
    dot_name += ".png"
    subprocess.call(["dot", "-Tpng", dot_file, "-o", dot_name])

    ast.semantic_analysis()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
