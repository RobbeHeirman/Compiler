"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

from typing import Dict, List

import Specifiers as TypeSpecifier
import messages as messages


class Attributes:
    """
    Container class used by SymbolTable to keep track of token Attributes
    """

    _base_type: TypeSpecifier.TypeSpecifier
    _operator_stack: List[TypeSpecifier.DeclaratorSpecifier]

    _column: int
    _line: int
    _filename: str

    def __init__(self, base_type: TypeSpecifier.TypeSpecifier, type_stack: List[TypeSpecifier.DeclaratorSpecifier],
                 filename: str, line: int, column: int, ):
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

    @property
    def filename(self)->str:
        return self._filename

    @filename.setter
    def filename(self, attr):
        self._filename = attr

    @property
    def line(self)->int:
        return self._line

    @line.setter
    def line(self, val):
        self._line = val

    @property
    def column(self)->int:
        return self._column

    @column.setter
    def column(self, val):
        self._column = val

    @property
    def decl_type(self):
        return self._base_type


class SymbolTable:
    """
    Represents the SymbolTable container used while parsing.
    """

    _container: Dict[str, Attributes]

    def __init__(self):
        self._container = dict()

    def add_id(self, lexeme: str, attribute: Attributes) -> bool:
        """
        Adds an id to the symbolic table. Returns True if adding was a success. Returns false if there is a parse error.
        For example redeclaration of a identifier is not allowed.

        :param attribute: an attribute container with all attributes of  the lexeme
        :param lexeme: The lexeme, the name of the identifier
        :return: True if this action is allowed, False if not.
        """

        if lexeme in self._container.keys():
            attr = self._container[lexeme]
            if attr.operator_stack and attribute.operator_stack:
                if attribute.operator_stack[-1] is TypeSpecifier.DeclaratorSpecifier.FUNC:
                    if attr.operator_stack[-1] is TypeSpecifier.DeclaratorSpecifier.FUNC:
                        return True

            messages.error_redeclaration(lexeme, attribute)
            attribute_prev = self._container[lexeme]
            messages.note_prev_decl(lexeme, attribute_prev)
            return False



        self._container[lexeme] = attribute
        return True

    def is_in_symbol_table(self, lexeme)->bool:
        """
        Checks if a lexeme is in the symbol table
        :param lexeme: the lexeme that needs to be checked.
        :return:
        """

        return lexeme in self._container.keys()

    def get_attribute(self, lexeme) -> Attributes:
        return self._container[lexeme]


class GlobalSymbolTable(SymbolTable):
    """
    Extension for global variable support
    """
    pass  # TODO: need to do something with this.
