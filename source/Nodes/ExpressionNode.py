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
    _failed: bool
    _children: List["AbstractNode"]

    def __init__(self, parent_node=None):
        super().__init__(parent_node)

        self._children = list()
        self._failed = False

    @property
    def failed(self)->bool:
        for child in self._children:
            self._fail_switch(child.failed)
        return self._failed

    def _fail_switch(self, boolean:bool):
        """
        used so that a node can tell parents there is a semantic error
        :param boolean: the boolean that tells if the expression failed.
        :return:
        """

        if boolean:
            self._failed = True

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

    def add_to_scope_symbol_table(self, lexeme: str, attribute: SymbolTable.Attributes) -> bool:
        """
        Hook to add a lexeme to symbol table. Child classes may need to implement this.
        We will just call the parents add symbol to scope. Scoped nodes contain SymbolTables and will look
        in their own table.
        :param lexeme: the lexeme we want to add.
        :param attribute Attribute object that describes the attributes of the lexeme.
        :return bool true if successfully added, false if not.
        """
        return self._parent_node.add_to_scope_symbol_table(lexeme, attribute)


    def generate_llvm(self) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        ret = ""

        for child in self._children:
            ret += child.generate_llvm()

        return ret
