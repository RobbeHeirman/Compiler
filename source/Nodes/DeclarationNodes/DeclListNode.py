"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from Nodes.DeclarationNodes.DeclarationNode import DeclarationNode
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import TypeSpecifier
from SymbolTable import Attributes


class DeclListNode(ExpressionNode):
    """
    Start of a , separated list of declarations.
    """
    _declaration_nodes: List[DeclarationNode]
    _base_type: TypeSpecifier
    _BASE_LABEL = "decl_list"

    def __init__(self, parent_node: AbstractNode):
        super().__init__(parent_node)

        self._base_type = None
        self._declaration_nodes = list()

    @property
    def base_type(self) -> TypeSpecifier:
        return self._base_type

    @property
    def label(self):
        return '{0}'.format(self._BASE_LABEL)

    def _add_base_type(self, child:BaseTypeNode):
        """
        Adds a base type node
        :param child: a base type node
        :type child: BaseTypeNode
        """

        self._base_type = child.value  # We are just interested in the base type, maybe this node needs to be ommited?

    def _add_declaration_node(self, child: DeclarationNode):
            self._declaration_nodes.append(child)
            child.base_type = self._base_type

    # This is how we mimic function overloading. Basicly the node needs to know what to do with his child.
    _ADD_OVERLOAD_MAP = {
        BaseTypeNode: _add_base_type,
        DeclarationNode: _add_declaration_node,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        self._ADD_OVERLOAD_MAP[type(child)](self, child)
        super().add_child(child)

    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes):

        attribute.type_spec = self._base_type
        super().add_to_scope_symbol_table(lexeme, attribute)