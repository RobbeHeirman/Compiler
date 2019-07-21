"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC

import Attributes
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import SymbolTable


class ScopedNode(AbstractNode.AbstractNode, ABC):
    """
    This node is an abstract node that presents all nodes with their own scope.
    This means this node has it's own SymbolTable
    """
    _register_index: int

    def __init__(self, parent_node=None, ctx=None):
        """
        Initializer
        """
        super().__init__(parent_node, ctx)
        self._symbol_table = SymbolTable.SymbolTable()
        self._register_index = -1

    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes.Attributes) -> bool:
        """
        This is a ScopedNode with own symbolTable. We will attempt to add to the symbol table here.
        :param lexeme: The lexeme (id name) of the variable we add
        :param attribute: set of attributes that describes the lexeme
        :return: boolean, true if successfully added, false if not.
        """

        return self._symbol_table.add_id(lexeme, attribute)

    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """
        if self._symbol_table.is_in_symbol_table(lexeme):
            return True

        else:
            return self._parent_node.is_in_table(lexeme)

    @property
    def register_index(self):
        return self._register_index

    def increment_register_index(self, amount=1):
        self._register_index += amount

    def get_attribute(self, lexeme):
        if self._symbol_table.is_in_symbol_table(lexeme):  # Is declared in this scope.
            return self._symbol_table.get_attribute(lexeme)

        else:
            return self._parent_node.get_attribute(lexeme)  # Looking in higher scoped symbol tables.

    def _is_global(self):
        return False
