"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""

import typing

import Specifiers
import messages as messages
import Attributes


class SymbolTable:
    """
    Represents the SymbolTable container used while parsing.
    """

    _container: typing.Dict[str, Attributes.Attributes]

    def __init__(self, messenger: messages.MessageGenerator):
        self._messenger = messenger
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
                if attribute.operator_stack[-1] is Specifiers.TypeModifier.FUNC:
                    if attr.operator_stack[-1] is Specifiers.TypeModifier.FUNC:
                        if attr.same_signature(attribute):
                            return True

            self._messenger.error_redeclaration(lexeme, attribute)
            attribute_prev = self._container[lexeme]
            self._messenger.note_prev_decl(lexeme, attribute_prev)
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


class GlobalSymbolTable(SymbolTable):
    """
    Extension for global variable support
    """
    pass  # TODO: need to do something with this.
