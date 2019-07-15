import typing

import Specifiers
import Specifiers as TypeSpecifier


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

    def __init__(self, type_stack: typing.List[Specifiers.TypeModifier],
                 filename: str, line: int, column: int):
        """
        Initializer
        :param type_stack: The operators applied on the declaration (*, [], ())
        :param filename: name of the file lexeme is found
        :param line: the line where de lexeme is found.
        :param column: the column where the lexeme is found.
        """

        self.operator_stack = type_stack  # Stacks all the declared operators operators
        self._filename = filename
        self._line = line
        self._column = column

    def __eq__(self, val: "Attributes") -> bool:
        if self.operator_stack == val.operator_stack:
            return True
        return False

    @property
    def base_type(self):
        return self._base_type

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
        return self.base_type

    # def same_signature(self, attr: "Attributes") -> bool:
    #     """
    #     Compares the function signatures of two attributes.
    #     :param attr: the attribute this attributes signature has to be compared against
    #     :return:
    #     """
    #
    #     if self.function_signature == attr.function_signature:
    #         return True
    #     return False

    # def rhs_same_signature(self, type_specs, error_attr, l_id):
    #
    #     own_list = [attr.decl_type for attr in self.function_signature]
    #
    #     if own_list == type_specs:
    #         return True
    #
    #     elif len(type_specs) < len(own_list):
    #         # self._messenger.error_func_to_few_arguments(l_id, error_attr)
    #         print("TODO Respect msg attributes")
    #     elif len(type_specs) > len(own_list):
    #         # self._messenger.error_func_to_many_arguments(l_id, error_attr)
    #         print("TODO Respect msg attributes")
    #     else:
    #         # self._messenger.error_signature_does_not_match(l_id, error_attr)
    #         print("TODO Respect msg attributes")
    #     return False


class AttributesGlobal(Attributes):
    """
    An extension on attributes for the global table
    """

    def __init__(self, type_stack: typing.List[Specifiers.TypeModifier], filename: str,
                 line: int, column: int, defined: bool, original_declaration_node):
        super().__init__(type_stack, filename, line, column)

        self.function_signature = []
        self.defined = defined

        self.original_declaration_node = original_declaration_node

    def __eq__(self, o):
        if super().__eq__(o):
            if self.function_signature == o.function_signature:
                return True
        return False
