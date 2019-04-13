"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC
import source.Nodes.ExpressionNode as ExpressionNode
from source.SymbolTable import SymbolTable, Attributes


class ScopedNode(ExpressionNode.ExpressionNode, ABC):
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

    def add_to_scope_symbol_table(self, lexeme: str,  attribute: Attributes)->bool:
        """
        This is a ScopedNode with own symbolTable. We will attempt to add to the symbol table here.
        :param lexeme: The lexeme (id name) of the variable we add
        :param attribute: set of attributes that describes the lexeme
        :return: boolean, true if successfully added, false if not.
        """

        return self._symbol_table.add_id(lexeme, attribute)
