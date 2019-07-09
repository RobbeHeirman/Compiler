"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Specifiers
import Attributes


class ColorScheme:
    # Color used
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class MessageGenerator:
    """
    Generates messages for the compiler. Keeps track of amount of error message calls.
    """

    def __init__(self):
        self.color_scheme = ColorScheme
        self._error_counter = 0
        self._warning_counter = 0



    @property
    def error_counter(self):
        return self._error_counter

    @property
    def warning_counter(self):
        return self._warning_counter

    @staticmethod
    def file_info(attribute: "Attributes.Attributes"):
        """Starter prints all info of where something should be told about"""

        filename = attribute.filename
        line = attribute.line
        column = attribute.column
        return MessageGenerator.file_info_f(filename, line, column)

    @staticmethod
    def file_info_f(filename, line, column):
        return "{0}:{1}:{2}: ".format(filename, line, column)

    def error(self, attribute: "Attributes.Attributes"):
        """Defines of type error"""
        return self.error_f(attribute.filename, attribute.line, attribute.column)

    def error_f(self, filename, line, column):
        self._error_counter += 1
        return "{0}error: ".format(MessageGenerator.file_info_f(filename, line, column))

    def error_redeclaration(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}redeclaration of \'{1}\' ".format(self.error(attribute), lexeme)
              + self.color_scheme.ENDC)

    def error_undeclared_var(self, lexeme, filename, line, column):
        print(self.color_scheme.FAIL + "{0}'{1}' undeclared".format(self.error_f(filename, line, column),
                                                                    lexeme) + self.color_scheme.ENDC)

    def error_redeclared_diff_symbol(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0} '{1}' redeclared as different kind of symbol".format(self.error(attribute),
                                                                                                 lexeme)
              + self.color_scheme.ENDC)

    def error_array_size_missing(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}array size missing in '{1}' ".format(self.error(attribute),
                                                                                lexeme) + self.color_scheme.ENDC)

    def error_invalid_initializer(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}invalid initializer".format(self.error(attribute),
                                                                       lexeme) + self.color_scheme.ENDC)

    def error_func_initialized_like_var(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}function '{1}' is initialized like a variable".format(self.error(attribute),
                                                                                                 lexeme)
              + self.color_scheme.ENDC)

    def error_subscript_not_array(self, attribute):
        print(self.color_scheme.FAIL + "{0}subscripted value isn't an array".format(self.error(attribute))
              + self.color_scheme.ENDC)

    def error_unary_not_ptr(self, attribute):
        print(self.color_scheme.FAIL + "{0}Invalid type argument of unary '*'".format(self.error(attribute))
              + self.color_scheme.ENDC)

    def error_object_not_function(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}called object '{1}' is not a function or function pointer".format(
            self.error(attribute),
            lexeme)
              + self.color_scheme.ENDC)

    def error_signature_does_not_match(self, lexeme, attribute):
        print(
            self.color_scheme.FAIL + "{0} function '{1}' signature does not match".format(self.error(attribute), lexeme)
            + self.color_scheme.ENDC)

    def error_func_to_few_arguments(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}too few arguments to function '{1}' ".format(self.error(attribute), lexeme)
              + self.color_scheme.ENDC)

    def error_func_to_many_arguments(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}too many arguments to function '{1}' ".format(self.error(attribute), lexeme)
              + self.color_scheme.ENDC)

    def error_lvalue_required_addr(self, attribute):
        print(self.color_scheme.FAIL + "{0}lvalue required as unary'&' operand".format(self.error(attribute))
              + self.color_scheme.ENDC)

    def error_non_void_return(self, lexeme, attribute):
        print(self.color_scheme.FAIL + "{0}non-void function '{1}' should return a value".format(self.error(attribute),
                                                                                                 lexeme)
              + self.color_scheme.ENDC)

    def error_no_conversion_int_ptr(self, attribute: "Attributes.Attributes",
                                    expression_type: Specifiers.TypeSpecifier):
        print(
            self.color_scheme.FAIL + "{0}incompatible pointer conversion initializing {1} * with an expression of "
                                     "type {2} "
            .format(self.error(attribute), attribute.decl_type.value, expression_type.value)
            + self.color_scheme.ENDC)

    def error_no_conversion_base_types(self, attribute: "Attributes.Attributes",
                                       expression_type: Specifiers.TypeSpecifier):
        print(self.color_scheme.FAIL + "{0}Cannot convert base types, initializing {1}  with an expression of type {2}"
              .format(self.error(attribute), attribute.decl_type.value, expression_type.value)
              + self.color_scheme.ENDC)

    def error_lvalue_required_addr_operand(self, filename, line, column):
        print(self.color_scheme.FAIL + "{0}lvalue required as unary '&' operand"
              .format(self.error_f(filename, line, column)) + self.color_scheme.ENDC)

    # Warnings
    # =======================================================================================================================
    def warning_f(self, filename, line, column):
        self._warning_counter += 1
        return self.color_scheme.WARNING + "{0}warning: ".format(MessageGenerator.file_info_f(filename, line, column))

    def warning_init_makes_a_from_b(self, a_type, b_type, filename, line, column):
        return "{0}initialization makes {1} from {2} without a cast".format(
            self.warning_f(filename, line, column), b_type, a_type) + self.color_scheme.ENDC

    @staticmethod
    def note(attribute: "Attributes.Attributes"):
        return "{0}note: ".format(MessageGenerator.file_info(attribute))

    def note_prev_decl(self, lexeme, attribute):
        return self.color_scheme.FAIL + "{0}previous declaration of \'{1}\' was here".format(
            MessageGenerator.note(attribute), lexeme) + self.color_scheme.ENDC
