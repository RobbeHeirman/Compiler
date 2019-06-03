"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import SymbolTable
from Specifiers import TypeSpecifier


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
    print(BColors.FAIL + "{0}'{1}' undeclared".format(error(attribute), lexeme) + BColors.ENDC)


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


def error_subscript_not_array(attribute):
    print(BColors.FAIL + "{0}subscripted value isn't an array".format(error(attribute))
          + BColors.ENDC)


def error_unary_not_ptr(attribute):
    print(BColors.FAIL + "{0}Invalid type argument of unary '*'".format(error(attribute))
          + BColors.ENDC)


def error_object_not_function(lexeme, attribute):
    print(BColors.FAIL + "{0}called object '{1}' is not a function or function pointer".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_signature_does_not_match(lexeme, attribute):
    print(BColors.FAIL + "{0} function '{1}' signature does not match".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_func_to_few_arguments(lexeme, attribute):
    print(BColors.FAIL + "{0}too few arguments to function '{1}' ".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_func_to_many_arguments(lexeme, attribute):
    print(BColors.FAIL + "{0}too many arguments to function '{1}' ".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_lvalue_required_addr(attribute):
    print(BColors.FAIL + "{0}lvalue required as unary'&' operand".format(error(attribute))
          + BColors.ENDC)


def error_non_void_return(lexeme, attribute):
    print(BColors.FAIL + "{0}non-void function '{1}' should return a value".format(error(attribute), lexeme)
          + BColors.ENDC)


def error_no_conversion_int_ptr(attribute: "SymbolTable.Attributes", expression_type: TypeSpecifier):
    print(BColors.FAIL + "{0}incompatible pointer conversion initializing {1} * with an expression of type {2}"
          .format(error(attribute), attribute.decl_type.value, expression_type.value)
          + BColors.ENDC)


def error_no_conversion_base_types(attribute: "SymbolTable.Attributes", expression_type: TypeSpecifier):
    print(BColors.FAIL + "{0}Cannot convert base types, initializing {1}  with an expression of type {2}"
          .format(error(attribute), attribute.decl_type.value, expression_type.value)
          + BColors.ENDC)


def note(attribute: "SymbolTable.Attributes"):
    return "{0}note: ".format(file_info(attribute))


def note_prev_decl(lexeme, attribute):
    print(BColors.FAIL + "{0}previous declaration of \'{1}\' was here".format(note(attribute), lexeme) + BColors.ENDC)
