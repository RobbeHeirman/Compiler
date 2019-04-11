"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
import string
from enum import Enum, auto
from typing import Dict, Any


class TypeSpecifier(Enum):
    """
    TypeSpecifier Attribute as Enum.
    Specifies a type for a identifier token.
    """
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'


class SymbolTable:
    """
    Represents the SymbolTable container used while parsing.
    """

    class Attributes:
        """
        Container class used by SymbolTable to keep track of token Attributes
        """

        type_spec: TypeSpecifier

        def __init__(self, type_spec: TypeSpecifier):
            """
            Initializer
            :param type_spec: The type_specifier attribute for this token.
            """

            self.type_spec = type_spec

    #_container: Dict[string, Attributes]

    def __init__(self):
        self._container = dict()

    def add_id(self, lexeme: string, type_spec) -> bool:
        """
        Adds an id to the symbolic table. Returns True if adding was a succes. Returns false if there is a parse error.
        For example redeclaration of a identifier is not allowed.

        :param lexeme: The lexeme, the name of the identifier
        :param type_spec: type of the identifier
        :return: True if this action is allowed, False if not.
        """

        if lexeme in self._container:
            print("Redecleration, TODO: Compile info (line, spot...")
            return False

        attr = SymbolTable.Attributes(type_spec)
        self._container[lexeme] = attr
        return True
