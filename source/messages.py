"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import sys


class ColorScheme:
    # Color used
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class MessageGenerator:
    """
    Generates messages for the compiler. Keeps track of amount of error message calls.
    """

    # Helpers init and properties
    # ==================================================================================================================

    def __init__(self, filename, string_stream=None):
        self._filename = filename

        self.color_scheme = ColorScheme
        self._error_counter = 0
        self._warning_counter = 0

        self._writer_c = string_stream if string_stream else sys.stdout

    @property
    def error_counter(self):
        return self._error_counter

    @property
    def warning_counter(self):
        return self._warning_counter

    def _writer(self, write_string):
        self._writer_c.write(f'{self.color_scheme.FAIL} {write_string} {self.color_scheme.ENDC}\n')

    def _file_info(self, line, column):
        return "{0}:{1}:{2}: ".format(self._filename, line, column)

    def _error(self, line, column):
        self._error_counter += 1
        return "{0}error: ".format(self._file_info(line, column))

    # Declaration error's
    # ==================================================================================================================
    def error_redeclaration(self, lexeme: str, line: int, column: int) -> None:
        """
        In local scope:
            int a;
            int a; // Not allowed.
        :param lexeme: id of variable with error
        :param line: line the line of the error
        :param column column of error
        """
        self._writer("{0}redeclaration of '{1}' ".format(self._error(line, column), lexeme))

    def error_redeclared_diff_symbol(self, lexeme: str, line: int, column: int) -> None:
        """
        in global scope:
            int a;
            char b = 44; // Not allowed.
        :param lexeme: id of variable with error
        :param line: line the line of the error
        :param column column of error
        """
        self._writer("{0} '{1}' redeclared as different kind of symbol".format(self._error(line, column), lexeme))

    def error_invalid_initializer(self, lexeme: str, line: int, column: int) -> None:
        """
        Any scope:
            int a = {0, 1 ,2,3} // a is not an array
            int b[] = 12 // Should use array initializer
        :param lexeme: id of variable with error
        :param line: line the line of the error
        :param column column of error
        """
        self._writer("{0}invalid initializer".format(self._error(line, column), lexeme))

    def error_init_is_not_constant(self, line: int, column: int) -> None:
        """
        Global scope:
            int a = 44;
            int b = a; // not allowed. globals should be initialized with compile-time constant.
        :param line: line the line of the error
        :param column column of error
        """
        self._writer(self._error(line, column) + "initializer element is not constant")

    # Errors in expression's
    # ==================================================================================================================

    def error_undeclared_var(self, lexeme: str, line: int, column: int) -> None:
        """
        Any scope:
            int a = b; // Not allowed, b is not declared
        :param lexeme: id of variable with error
        :param line: line the line of the error
        :param column column of error
        """
        self._writer("{0}'{1}' undeclared".format(self._error(line, column), lexeme))

    def error_unary_not_ptr(self, line, column):
        self._writer("{0}Invalid type argument of unary '*'".format(self._error(line, column)))

    def error_object_not_function(self, line, column):
        self._writer(f"{self._error(line, column)}called object is not a function or function pointer")

    def error_lvalue_required_addr(self, line, column):
        self._writer("{0}lvalue required as unary'&' operand".format(self._error(line, column)))

    def error_no_conversion_int_ptr(self, expression_type1, expression_type2, line, column):
        self._writer("{0}incompatible pointer conversion initializing {1} * with an expression of " "type {2} "
                     .format(self._error(line, column), expression_type1.value, expression_type2.value))

    def error_no_conversion_base_types(self, expression_type1, expression_type2, line, column):
        self._writer("{0}Cannot convert base types, initializing {1}  with an expression of type {2}".format(
            self._error(line, column), expression_type1.value, expression_type2.value))

    def error_conflicting_types(self, line, column, node_id):
        self._writer(self._error(line, column) + "conflicting types for '" + str(node_id) + "'")

    # Error's in assignment's
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def error_expected_l_value(self, line, column):
        self._writer(self._error(line, column) + 'lvalue required as left operand of assignment')
    # Function declaration, definition and call error's
    # ==================================================================================================================
    def error_func_initialized_like_var(self, lexeme, line, column):
        self._writer("{0}function '{1}' is initialized like a variable".format(self._error(line, column), lexeme))

    def error_signature_does_not_match(self, line, column):
        self._writer("{0} function signature does not match".format(self._error(line, column)))

    def error_func_to_few_arguments(self, lexeme, line, column):
        self._writer("{0}too few arguments to function '{1}' ".format(self._error(line, column), lexeme))

    def error_func_to_many_arguments(self, lexeme, line, column):
        self._writer("{0}too many arguments to function '{1}' ".format(self._error(line, column), lexeme))

    def error_non_void_return(self, lexeme, line, column):
        self._writer("{0}non-void function '{1}' should return a value".format(self._error(line, column), lexeme))

    def error_redefinition(self, line, column, id_i):
        self._writer(self._error(line, column) + "redefinition of '" + str(id_i) + "'")

    def error_conflicting_return_type(self, line, column):
        self._writer("{0}conflicting return types".format(self._error(line, column)))

    # Array's
    # ==================================================================================================================
    def error_size_not_integer(self, lexeme, line, column):
        self._writer(f'{self._error(line, column)}size of array \'{lexeme}\' has non-integer type')

    def error_array_size_missing(self, lexeme, line, column):
        self._writer("{0}array size missing in '{1}' ".format(self._error(line, column), lexeme))

    def error_subscript_not_array(self, line, column):
        self._writer("{0}subscripted value isn't an array".format(self._error(line, column)))

    # Warnings
    # ==================================================================================================================
    def warning(self, line, column):
        self._warning_counter += 1
        return "{0}warning: ".format(self._file_info(line, column))

    def warning_init_makes_a_from_b(self, a_type, b_type, line, column):
        self._writer(f"{self.warning(line, column)}initialization makes {a_type} from {b_type} without a cast")

    def note(self, line, column):
        return "{0}note: ".format(self._file_info(line, column))

    def note_prev_decl(self, lexeme, line, column):
        self._writer("{0}previous declaration of \'{1}\' was here".format(self.note(line, column), lexeme))
