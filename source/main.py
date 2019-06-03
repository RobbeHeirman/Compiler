"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
import subprocess
import sys
import traceback

from antlr4 import *

from gen.CLexer import CLexer
from gen.CParser import CParser
import CListenerExtend as CListenerExtend


class TracePrints(object):
    def __init__(self):
        self.stdout = sys.stdout

    def write(self, s):
        self.stdout.write("Writing %r\n" % s)
        traceback.print_stack(file=self.stdout)


# sys.stdout = TracePrints()
def main(argv):
    # Lexical analysis
    # input_file = argv[0]
    input_file = argv[1]
    input_stream = FileStream(input_file)
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.statements()
    if parser.getNumberOfSyntaxErrors() is not 0:
        return 1

    listener = CListenerExtend.CListenerExtend(input_file)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Initial AST (Used for debugging)
    ast = listener.ast
    dot_file = "AST.dot"
    if len(argv) == 3:
        dot_file = argv[2]
    ast.to_dot(dot_file)
    dot_name = dot_file[0: -4]
    dot_name += ".png"
    subprocess.call(["dot", "-Tpng", dot_file, "-o", dot_name])

    # Ast cleanup
    ast.first_pass()
    dot_file = "AST2.dot"
    ast.to_dot(dot_file)
    dot_name = dot_file[0: -4]
    dot_name += ".png"
    subprocess.call(["dot", "-Tpng", dot_file, "-o", dot_name])

    if not ast.semantic_analysis():
        print("I failed =(")
    else:
        file_name = argv[2]
        file = open(file_name, 'w+')

        target_triple = subprocess.check_output(["clang", "-print-target-triple"])
        target_triple = str(target_triple[0:-1])
        target_triple = 'target triple = "{0}"\n'.format(target_triple[2:])
        file.write(target_triple)
        file.write(ast.generate_llvm())
        file.close()

        print("Normal clang compile...")
        subprocess.call(["clang", input_file, "-S", "-emit-llvm"])  # Test compiler errors
        print("Done with clang compiling.")
        print("Assembling own IR llvm...")
        subprocess.call(["clang", "-Wno-override-module", "C_files/llvm.ll"])  # Test llvm generated language
        print("Done with llvm assembling")
        print("Running executable..")
        child = subprocess.Popen(["a.exe"])
        stream = child.communicate()[0]
        print(child.returncode)
        print("Done running executable")

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
