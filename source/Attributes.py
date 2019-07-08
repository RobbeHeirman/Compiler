import typing

import Specifiers
import Specifiers as TypeSpecifier
import messages as messages


class Attributes:
    """
    Container class used by SymbolTable to keep track of token Attributes
    """
    function_signature: typing.List["Attributes"]

    _base_type: TypeSpecifier
    _operator_stack: typing.List[Specifiers.TypeModifier]

    _column: int
    _line: int
    _filename: str

    def __init__(self, base_type: TypeSpecifier, type_stack: typing.List[Specifiers.TypeModifier],
                 filename: str, line: int, column: int, messenger: messages.MessageGenerator):
        """
        Initializer
        :param base_type: The type_specifier attribute for this token.
        :param type_stack: The operators applied on the declaration (*, [], ())
        :param filename: name of the file lexeme is found
        :param line: the line where de lexeme is found.
        :param column: the column where the lexeme is found.
        """

        self._base_type = base_type
        self.operator_stack = type_stack  # Stacks all the declared operators operators
        self._filename = filename
        self._line = line
        self._column = column
        self.function_signature = []

        self._messenger = messenger

    def __eq__(self, val: "Attributes") -> bool:

        if self._base_type == val._base_type:
            if self.operator_stack == val.operator_stack:
                return True
        return False

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, attr):
        self._filename = attr

    @property
    def line(self) -> int:
        return self._line

    @line.setter
    def line(self, val):
        self._line = val

    @property
    def column(self) -> int:
        return self._column

    @column.setter
    def column(self, val):
        self._column = val

    @property
    def decl_type(self):
        return self._base_type

    def same_signature(self, attr: "Attributes") -> bool:
        """
        Compares the function signatures of two attributes.
        :param attr: the attribute this attributes signature has to be compared against
        :return:
        """

        if self.function_signature == attr.function_signature:
            return True
        return False

    def rhs_same_signature(self, type_specs, error_attr, l_id):

        own_list = [attr.decl_type for attr in self.function_signature]

        if own_list == type_specs:
            return True

        elif len(type_specs) < len(own_list):
            self._messenger.error_func_to_few_arguments(l_id, error_attr)

        elif len(type_specs) > len(own_list):
            self._messenger.error_func_to_many_arguments(l_id, error_attr)

        else:
            self._messenger.error_signature_does_not_match(l_id, error_attr)

        return False