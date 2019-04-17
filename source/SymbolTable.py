"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

from typing import Dict

import source.Specifiers as TypeSpecifier
import source.messages as messages


class Attributes:
    """
    Container class used by SymbolTable to keep track of token Attributes
    """
    _column: int
    _line: int
    _filename: str
    _type_spec: TypeSpecifier.TypeSpecifier

    def __init__(self, type_spec: TypeSpecifier.TypeSpecifier, filename: str, line: int, column: int):
        """
        Initializer
        :param type_spec: The type_specifier attribute for this token.
        :param filename: name of the file lexeme is found
        :param line: the line where de lexeme is found.
        :param column: the column where the lexeme is found.
        """

        self._type_spec = type_spec
        self._filename = filename
        self._line = line
        self._column = column

    @property
    def filename(self)->str:
        return self._filename

    @property
    def line(self)->int:
        return self._line

    @property
    def column(self)->int:
        return self._column

    @property
    def type_spec(self):
        return self._type_spec

    @type_spec.setter
    def type_spec(self, value):
        self._type_spec = value


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
