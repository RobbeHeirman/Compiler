"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode


class RootNode(ScopedNode.ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"

    def __init__(self):
        super().__init__()

    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """

        return self._symbol_table.is_in_symbol_table(lexeme)

    def get_attribute(self, lexeme):
        return self._symbol_table.get_attribute(lexeme)
