"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List
from source.Nodes.BaseTypeNode import BaseTypeNode
from source.Nodes.ConstantNode import ConstantNode
from source.Nodes.DeclaratorNode import DeclaratorNode
from source.Nodes.AbstractNode import AbstractNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.SymbolTable import Attributes


class DeclarationNode(ExpressionNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _lexeme: str
    _declarator_list: List[DeclaratorNode]
    _base_type_node: BaseTypeNode

    label = "Declaration"

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._base_type_node = None
        self._declarator_list = []
        self._id = None

    @property
    def id(self):
        return self._id

    def _add_base_type(self, child: BaseTypeNode):
        """
        Adds a base type child
        :param child: BaseTypeChild add a BaseTypeNode
        """
        self._base_type_node = child

    def _add_declarator(self, child: DeclaratorNode):
        self._declarator_list.append(child)
        self._id = child.value
        self._declare_variable(child)

    def _add_constant(self, child):
        pass

    _add_overload_map = {
        BaseTypeNode: _add_base_type,
        DeclaratorNode: _add_declarator,
        ConstantNode: _add_constant,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode._add_overload_map[type(child)](self, child)
        super().add_child(child)

    def _declare_variable(self, node: DeclaratorNode):

        filename = node.filename
        line = node.line
        column = node.column
        type_spec = self._base_type_node.value
        lexeme = node.value
        attribute = Attributes(type_spec, filename, line, column)

        if not self.add_to_scope_symbol_table(lexeme, attribute):
            self._fail_switch(True)

    def generate_llvm(self)->str:
        """
        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}
        :return: the generated string
        """
        ret = ""

        type_spec = self._base_type_node.value
        for declarator in self._declarator_list:
            lexeme = declarator.value
            ret += "%{0} = alloca {1}, align {2}\n".format(lexeme, type_spec.llvm_type, type_spec.llvm_alignment)

        return ret
