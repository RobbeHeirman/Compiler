"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.AbstractNode import AbstractNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.Specifiers import TypeSpecifier


class DeclListNode(ExpressionNode):
    """
    Start of a , separated list of declarations.
    """
    _base_type: TypeSpecifier
    label = "decl_list"

    def __init__(self, parent_node: AbstractNode):
        super().__init__(parent_node)

        self._base_type = None

    @property
    def base_type(self) -> TypeSpecifier:
        return self._base_type

    @base_type.setter
    def base_type(self, value: TypeSpecifier):
        self._base_type = value
