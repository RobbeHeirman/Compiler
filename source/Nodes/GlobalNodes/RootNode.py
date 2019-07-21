"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode
import SymbolTable


class RootNode(ScopedNode.ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"

    def __init__(self, ctx):
        super().__init__(None, ctx)

        self._symbol_table = SymbolTable.GlobalSymbolTable()

    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """

        return self._symbol_table.is_in_symbol_table(lexeme)

    def get_attribute(self, lexeme):
        return self._symbol_table.get_attribute(lexeme)

    def _is_global(self):
        return True
