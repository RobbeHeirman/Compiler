"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod
from typing import List

import source.Nodes.AbstractNode as AbstractNode
import source.SymbolTable as SymbolTable


class ExpressionNode(AbstractNode.AbstractNode, ABC):
    """
    Abstract node for all intermediate "expression" nodes. Complements leaf node
    """
    _children: List["AbstractNode"]

    def __init__(self, parent_node=None):
        super().__init__(parent_node)

        self._children = list()

    def add_child(self, child: "AbstractNode"):
        """
        Add a child node to the AST.
        :param child: a ASTNode that functions as a child
        """

        self._children.append(child)

    def dot_string(self) -> str:
        """Generates the visual representation of the node in .dot"""
        ret = super().dot_string()

        ret += "{0}--{{".format(self._index)
        for child in self._children:
            ret += "{0} ".format(child.index)

        ret += "}\n"

        for child in self._children:
            ret += child.dot_string()

        return ret

    def add_to_scope_symbol_table(self, lexeme: str, attribute: SymbolTable.Attributes)->bool:
        """
        Hook to add a lexeme to symbol table. Child classes may need to implement this.
        We will just call the parents add symbol to scope. Scoped nodes contain SymbolTables and will look
        in their own table.
        :param lexeme: the lexeme we want to add.
        :param attribute Attribute object that describes the attributes of the lexeme.
        :return bool true if successfully added, false if not.
        """
        return self._parent_node.add_to_scope_symbol_table(lexeme, attribute)

    @abstractmethod
    def resolve_expression(self):
        """
        Resolves an expression node. Depending on the expression that needs to be resolved
        """
        pass

    def generate_llvm(self)->str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        pass