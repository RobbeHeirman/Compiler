Author: Robbe Heirman

Description:
            Compiler of small C following the specification given in tasks/C2Mips_ProjectDescription
            Not implemented: Type conversion dynamic and multi-dimensional arrays. Keywords switch and default
                             Constant propagation (folding == ok)
                             Global variable doesn't work properly in MIP assembly.

How to use:
        the 'build.py' script when run generates the lexer, parser and walker code.
        Needed to parse the given file. Must be run from compiler dir
        when using the compiler for the first time Or when changing the corresponding Grammars/C.g4 file.

        the 'compiler.py' script requires a input .C file and will by default generated a .ll and .asm file.
        the .ll and .asm file are translations of the c file to llvm ir and MIPS assembly.
        Additional options can be specified. (Specified in next paragraph). All files require to be in
        their relative position as they are.

positional arguments:
  input_file            The required C file to compile

optional arguments:
  -h, --help            show this help message and exit
  -visual_ast           Generate a png that visualizes the ast. DOT required
  -no_llvm              If flag is specified there will be no llvm code
                        generation
  -no_mips              If flag is specified there will be no mips code
                        generation
  -ref_test             Generates a LLVM ref
                        (only works with clang installed)
  -executable_test_llvm Makes a executable from generated llvm, Runs the exec.
                        (only works with clang installed)
  -executable_test_mips Runs the generated Mips code trough the Mars simulator.
                        Requires the mars in compiler dir under name Mars.jar.
  -test                 Runs entire test suite.