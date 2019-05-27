"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import SymbolTable


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def file_info(attribute: "SymbolTable.Attributes"):
    """Starter prints all info of where something should be told about"""

    filename = attribute.filename
    line = attribute.line
    column = attribute.column

    return "{0}:{1}:{2}: ".format(filename, line, column)


def error(attribute: "SymbolTable.Attributes"):
    """Defines of type error"""
    return "{0}error: ".format(file_info(attribute))


def error_redeclaration(lexeme, attribute):
    print(BColors.FAIL + "{0}redeclaration of \'{1}\' ".format(error(attribute), lexeme) + BColors.ENDC)


def error_undeclared_var(lexeme, attribute):
    print(BColors.FAIL + "{0}{1} undeclared".format(error(attribute), lexeme) + BColors.ENDC)


def error_redeclared_diff_symbol(lexeme, attribute):
    print(BColors.FAIL + "{0} '{1}' redeclared as different kind of symbol".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_array_size_missing(lexeme, attribute):
    print(BColors.FAIL + "{0}array size missing in '{1}' ".format(error(attribute), lexeme) + BColors.ENDC)


def error_invalid_initializer(lexeme, attribute):
    print(BColors.FAIL + "{0}invalid initializer".format(error(attribute), lexeme) + BColors.ENDC)


def error_func_initialized_like_var(lexeme, attribute):
    print(BColors.FAIL + "{0}function '{1}' is initialized like a variable".format(error(attribute), lexeme)
          + BColors.ENDC)


def note(attribute: "SymbolTable.Attributes"):
    return "{0}note: ".format(file_info(attribute))


def note_prev_decl(lexeme, attribute):
    print(BColors.FAIL + "{0}previous declaration of \'{1}\' was here".format(note(attribute), lexeme) + BColors.ENDC)
