"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Any

from source.Nodes.AbstractNode import AbstractNode
from source.Nodes.BaseTypeNode import BaseTypeNode
from source.Nodes.DeclarationNode import DeclarationNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.Specifiers import TypeSpecifier


class DeclListNode(ExpressionNode):
    """
    Start of a , separated list of declarations.
    """
    _declaration_nodes: List[DeclarationNode]
    _base_type: TypeSpecifier
    label = "decl_list"

    def __init__(self, parent_node: AbstractNode):
        super().__init__(parent_node)

        self._base_type = None
        self._declaration_nodes = list()

    @property
    def base_type(self) -> TypeSpecifier:
        return self._base_type

    def _add_base_type(self, child:BaseTypeNode):
        """
        Adds a base type node
        :param child: a base type node
        :type child: BaseTypeNode
        """

        self._base_type = child.value

    def _add_declaration_node(self, child:DeclarationNode):
            self._declaration_nodes.append(child)

    _ADD_OVERLOAD_MAP = {
        BaseTypeNode: _add_base_type,
        DeclarationNode: _add_declaration_node,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        self._ADD_OVERLOAD_MAP[type(child)](self, child)
        super().add_child(child)

    def handle_semantics(self):
        for child in self._declaration_nodes:
            child.declare_variable(self._base_type)