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
from source.SymbolTable import Attributes


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

    _add_overload_map = {
        BaseTypeNode: _add_base_type,
        DeclaratorNode: _add_declarator,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode._add_overload_map[type(child)](self, child)
        super().add_child(child)

    def resolve_expression(self) -> bool:
        """
        Adding to the symbol table in case of a declaration.
        :return: bool: true if everything worked correctly false else.
        """
        type_spec = self._base_type_node.value
        success = True

        for node in self._declarator_list:

            filename = node.filename
            line = node.line
            column = node.column
            lexeme = node.value
            attribute = Attributes(type_spec, filename, line, column)

            if not self.add_to_scope_symbol_table(lexeme, attribute):
                success = False

        return success
