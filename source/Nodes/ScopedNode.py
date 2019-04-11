"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC
from source.Nodes.AbstractNode import AbstractNode
from source.SymbolTable import SymbolTable


class ScopedNode(AbstractNode, ABC):
    """
    This node is an abstract node that presents all nodes with their own scope.
    This means this node has it's own SymbolTable
    """
    def __init__(self):
        """
        Initializer
        """
        super().__init__()
        self._symbol_table = SymbolTable()
