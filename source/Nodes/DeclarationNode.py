"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List
from source.Nodes.BaseTypeNode import BaseTypeNode
from source.Nodes.DeclaratorNode import DeclaratorNode
from source.Nodes.AbstractNode import AbstractNode
from source.Nodes.ExpressionNode import ExpressionNode


class DeclarationNode(ExpressionNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _declarator_list: List[DeclaratorNode]
    _base_type_node: BaseTypeNode

    label = "Declaration"

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._base_type_node = None
        self._declarator_list = []

    def _add_base_type(self, child: BaseTypeNode):
        """
        Adds a base type child
        :param child: BaseTypeChild add a BaseTypeNode
        """
        self._base_type_node = child

    def _add_declarator(self, child: DeclaratorNode):
        self._declarator_list.append(child)

    add_overload_map = {
        BaseTypeNode: _add_base_type,
        DeclaratorNode: _add_declarator,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode.add_overload_map[type(child)](self, child)
        super().add_child(child)
