"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
import os
import subprocess
from importlib import util

from antlr4 import *
import AST

from gen.CLexer import CLexer
from gen.CParser import CParser
import CListenerExtend as CListenerExtend


def create_ast(input_file: str, string_stream=None) -> AST.AST:
    """
    Function will create the AST from the listener and returns the ast
    :param input_file: is the name of the input C file
    :param string_stream: a possible string stream to write errors to
    :return: the corresponding AST
    """

    input_stream = FileStream(input_file)
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.root()

    listener = CListenerExtend.CListenerExtend(input_file, string_stream)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.ast


def generate_ast_visuals(ast: AST, output_path_slug):
    """
    Generates a visual png file from the AST to the specified output_filename
    :param ast: The ast we want to visualize
    :param output_path_slug: The path + slug. Will be extended by png
    :return: No return, files get generated on output_filename
    """

    ast.to_dot("temp.dot")
    png_name = output_path_slug + ".png"
    subprocess.call(["dot", "-Tpng", "temp.dot", "-o", png_name])
    os.remove("temp.dot")


def generate_llvm(ast: AST, output_path_slug):
    """
    Generates corresponding llvm_code
    :param ast: the ast where we generate code from
    :param output_path_slug: the slug of the output path.
    :return: Nothing will be written to output_file
    """
    file_name = output_path_slug + ".ll"
    file = open(file_name, 'w+')
    file.write(ast.generate_llvm())
    file.close()


def generate_mips(ast: AST, output_path_slug):
    file_name = output_path_slug + ".asm"
    file = open(file_name, 'w+')
    file.write(ast.generate_mips())
    file.close()
