import argparse
import subprocess
import sys
import os
import shutil
from inspect import stack
import main


class TracePrints(object):
    def __init__(self):
        self.stdout = sys.stdout

    def write(self, s):
        if s != '\n':
            frame_info = stack()[1]
            type(frame_info)
            self.stdout.write(f'{frame_info[1]}:{frame_info[2]}: {s}\n')

    def flush(self):
        self.stdout.flush()


sys.stdout = TracePrints()

if __name__ == "__main__":

    # Set-up
    # ==================================================================================================================
    # Cleaning up previous run
    if os.path.exists("result/"):
        shutil.rmtree("result/")

    cmd_parser = argparse.ArgumentParser(description="Compiles C file to LLVM intermediate language")

    cmd_parser.add_argument("-visual_ast", help="Generate a png that visualizes the ast. DOT required",
                            action="store_true")

    # Argument parsing
    cmd_parser.add_argument("input_file", nargs="?", default=-1, help="The required C file to compile")
    cmd_parser.add_argument("-no_llvm", help="If flag is specified there will be no llvm code generation",
                            action="store_true")
    cmd_parser.add_argument("-no_mips", help="If flag is specified there will be no mips code generation",
                            action="store_true")
    cmd_parser.add_argument("-ref_test", action="store_true")
    cmd_parser.add_argument("-executable_test_llvm", action="store_true")
    cmd_parser.add_argument("-executable_test_mips", action="store_true")
    cmd_parser.add_argument("-test", action="store_true")

    args = cmd_parser.parse_args()

    if args.test:
        try:
            subprocess.call(["python3", "-m", "unittest", "discover", "-p", "*_test.py"])
        except FileNotFoundError:
            subprocess.call(["python", "-m", "unittest", "discover", "-p", "*_test.py"])
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

    # AST generation
    # ==================================================================================================================
    # Creating AST
    ast = main.create_ast(args.input_file)

    if ast == -1:
        print("Syntax errors")
        sys.exit(1)

    if args.visual_ast:
        os.makedirs(path + "AST")
        main.generate_ast_visuals(ast, path + "AST/" + slug + "_pre_folding")

    ast.constant_folding()

    if args.visual_ast:
        main.generate_ast_visuals(ast, path + "AST/" + slug + "_pre_analysis")

    # If the semantic analysis fails
    if not ast.semantic_analysis():
        print("incorrect analysis")
        sys.exit(1)

    if args.visual_ast:
        main.generate_ast_visuals(ast, path + "AST/" + slug + "_post_analysis")

    # Code generation
    # ==================================================================================================================
    # generate the ll code
    if not args.no_llvm:
        main.generate_llvm(ast, path + slug)

    if not args.no_mips:
        main.generate_mips(ast, path + slug)

    # Ref tests
    # ==================================================================================================================
    if args.ref_test:
        name_reference = path + slug + "_ref.ll"
        subprocess.call(["clang", "-cc1", args.input_file, "-emit-llvm", "-Wall", "-Wpedantic", "-Wconversion",
                         "-o", name_reference])  # Test compiler errors

    # Run executables
    # ==================================================================================================================
    if args.executable_test_llvm:
        ll_file = path + slug + ".ll"
        # Test llvm generated language
        runner = subprocess.run(["clang", "-Wno-override-module", ll_file, "-o", path + slug + ".exe"])

        code = subprocess.call(["./" + path + slug + ".exe"])
        print(f'Return code of tested llvm = {code}')

    if args.executable_test_mips:
        code = subprocess.call(["java", "-jar", "Mars.jar", "nc", path + slug + ".asm"])
        print(f'Return code of tested MIPS = {code}')
    sys.exit(0)
