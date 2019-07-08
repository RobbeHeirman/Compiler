#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import shutil

import main

if __name__ == "__main__":
    # Cleaning up previous run
    if os.path.exists("result/"):
        shutil.rmtree("result/")

    # Argument parsing
    cmd_parser = argparse.ArgumentParser(description="Compiles C file to LLVM intermediate language")
    cmd_parser.add_argument("input_file", nargs="?", default=-1, help="The required C file to compile")
    cmd_parser.add_argument("-visual_ast", help="Generate a png that visualizes the ast. DOT required",
                            action="store_true")
    cmd_parser.add_argument("-no_code", help="If flag is specified there will be no code generation",
                            action="store_true")
    cmd_parser.add_argument("-ref_test", action="store_true")
    cmd_parser.add_argument("-executable_test", action="store_true")
    cmd_parser.add_argument("-test", action="store_true")

    args = cmd_parser.parse_args()

    if args.test:
        subprocess.call(["python3", "-m", "unittest", "discover", "-p", "*_test.py"])
        sys.exit(0)

    if args.input_file is -1:
        print("Please specify input file")
        sys.exit(1)

    # Slug is useful for naming consistency of output files
    slug = os.path.basename(args.input_file)[:-2]

    # Setting up target directory
    path = "result/" + slug + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Creating AST
    ast = main.create_ast(args.input_file)

    # Visuals
    if args.visual_ast:
        main.generate_ast_visuals(ast, path + slug)
        ast.first_pass()  # Some cleanup hope to deprecate this
        main.generate_ast_visuals(ast, path + slug + "2")

    # If the semantic analysis fails
    if ast.semantic_analysis() is False:
        sys.exit(1)

    # generate the ll code
    if not args.no_code:
        main.generate_llvm(ast, path + slug)

    if args.ref_test:
        name_reference = path + slug + "_ref.ll"
        subprocess.call(["clang", args.input_file, "-S", "-emit-llvm", "-o", name_reference])  # Test compiler errors

    if args.executable_test:
        ll_file = path + slug + ".ll"
        # Test llvm generated language
        runner = subprocess.run(["clang", "-Wno-override-module", ll_file, "-o", path + slug + ".exe"])
        if runner.returncode is 0:
            subprocess.call(["./a.exe"])

    sys.exit(0)
