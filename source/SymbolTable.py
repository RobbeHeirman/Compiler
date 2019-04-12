"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

from typing import Dict

from source.Specifiers import TypeSpecifier


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


class SymbolTable:
    """
    Represents the SymbolTable container used while parsing.
    """

    _container: Dict[str, Attributes]

    def __init__(self):
        self._container = dict()

    def add_id(self, lexeme: str, attribute:Attributes) -> bool:
        """
        Adds an id to the symbolic table. Returns True if adding was a succes. Returns false if there is a parse error.
        For example redeclaration of a identifier is not allowed.

        :param attribute: an attribute container with all attributes of  the lexeme
        :param lexeme: The lexeme, the name of the identifier
        :return: True if this action is allowed, False if not.
        """

        if lexeme in self._container:
            print("Redeclaration, TODO: Compile info (line, spot...")
            return False

        self._container[lexeme] = attribute
        return True
