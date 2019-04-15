"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC
from typing import List

import source.Nodes.AbstractNode as AbstractNode


class ExpressionNode(AbstractNode.AbstractNode, ABC):
    """
    Abstract node for all intermediate "expression" nodes. Complements leaf node
    """
    _failed: bool
    _children: List["AbstractNode"]

    def __init__(self, parent_node=None):
        super().__init__(parent_node)

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

    def is_in_table(self, lexeme: str) -> bool:
        return self._parent_node.is_in_table(lexeme)

    def generate_llvm(self) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        ret = ""
        for child in self._children:
            ret += child.generate_llvm()

        return ret