"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

import typing
from enum import Enum, auto
import Attributes


class SymbolTable:
    """
    Represents the SymbolTable container used while parsing.
    """

    _container: typing.Dict[str, Attributes.Attributes]

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
            return False
        self._container[lexeme] = attribute
        return True

    def is_in_symbol_table(self, lexeme) -> bool:
        """
        Checks if a lexeme is in the symbol table
        :param lexeme: the lexeme that needs to be checked.
        :return:
        """

        return lexeme in self._container.keys()

    def get_attribute(self, lexeme) -> Attributes:
        return self._container.get(lexeme, False)


class GlobalActions(Enum):
    """In a the global case, there are 3 actions. Do nothing, redefining error, define prev declared."""

    DO_NOTHING = auto()
    REMOVE_NODE = auto()  # OPT: some redeclaration's just don't do anything, we can remove those nodes from the AST
    WRONG_TYPE = auto()
    REDEFINE_ERROR = auto()
    # This is a special case. We need to restructure the AST so the definition happens on the first declare.
    DEFINE_PREV_DECLARED = ()

class GlobalSymbolTable(SymbolTable):
    """
    Extension for global variable support
    """
    _container: typing.Dict[str, Attributes.AttributesGlobal]

    def add_id(self, lexeme: str, attribute: Attributes.AttributesGlobal) -> GlobalActions:
        """
        Adds an id to the symbolic table. Returns True if adding was a success. Returns false if there is a parse error.
        For example redeclaration of a identifier is not allowed.

        :param attribute: an attribute container with all attributes of  the lexeme
        :param lexeme: The lexeme, the name of the identifier
        :return: True if this action is allowed, False if not.
        """
        # In the global case we can declare as much as we want, but only define once.
        if lexeme in self._container.keys():
            attr = self._container[lexeme]

            # We check if the redeclaration has the same type.
            if attribute != attr:
                return GlobalActions.WRONG_TYPE

            # We can safely ignore a non defining redeclaration
            if not attribute.defined:
                # OPT: some redeclaration's just don't do anything, we can remove those nodes from the AST
                return GlobalActions.REMOVE_NODE

            else:
                # The following actions depend on the value in the already existing identifier

                # The value is already defined, so this is an error.
                if attr.defined:
                    return GlobalActions.REDEFINE_ERROR

                # The node of the AST needs to undertake special action's because we just want to define it once.
                else:
                    return GlobalActions.DEFINE_PREV_DECLARED

        # Not in table yet so we can safely add it.

        self._container[lexeme] = attribute
        return GlobalActions.DO_NOTHING
