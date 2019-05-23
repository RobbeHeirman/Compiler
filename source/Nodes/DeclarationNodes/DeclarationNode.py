"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.ExpressionNodes.ConstantNode import ConstantNode
from Nodes.ExpressionNodes.IdNode import IdNode
from Nodes.ExpressionNodes.RHSNode import RHSNode
from Nodes.DeclarationNodes.DeclaratorNode import DeclaratorNode
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import TypeSpecifier
from SymbolTable import Attributes
from typing import Union


class DeclarationNode(ExpressionNode):
    """
    Represents a Declaration in our abstract syntax tree.
    Will deduct the base type of the declaration in the first pass.
    Has 1 or 2 children a declarator (will become a stack of pre and postfix type specifiers after first pass)
    An optional initializer as 2d child.
    """
    _lexeme: str
    _declarator_list: DeclaratorNode

    _BASE_LABEL = "Declaration"

    def __init__(self, parent_node: ExpressionNode):
        super().__init__(parent_node)

        # The 2 child nodes
        self._declarator_node = None
        self._rhs_node = None

        self._id = None  # Id can be deducted from children.
        self._base_type = None  # Base type gets passed from a decl_list node.

    @property
    def label(self):
        ret_label = self._BASE_LABEL
        if self._base_type is not None:
            ret_label += "\\nBase type: {0}".format(self._base_type.value)

        return ret_label

    @property
    def id(self):
        return self._id

    @property
    def base_type(self):
        return self._base_type

    @base_type.setter
    def base_type(self, value: TypeSpecifier):
        self._base_type = value

    def _add_declarator(self, child: DeclaratorNode):
        self._declarator_node = child

    def _add_rhs(self, child):
        self._rhs_node = child

    # Can we do something to make overloading more generic
    _add_overload_map = {
        DeclaratorNode: _add_declarator,
        RHSNode: _add_rhs,
        ConstantNode: _add_rhs,
        IdNode: _add_rhs
    }

    def add_child(self, child: Union[DeclaratorNode, RHSNode]):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode._add_overload_map.get(type(child))(self, child)
        super().add_child(child)

    def first_pass(self):
        """
        Mainly used for node cleanup. We can remove all the "Declarator stub nodes. They were mainly there
        to handle typeSpecifier hierarchy
        """

        # TODO: find the id in the declaration_node

        self._declarator_node.first_pass()

    """def declare_variable(self, base_type: TypeSpecifier):

        self._base_type = base_type
        node = self._children[0]
        filename = node.filename
        line = node.line
        column = node.column
        type_spec = self._base_type
        lexeme = node.value
        attribute = Attributes(type_spec, filename, line, column)

        if not self.add_to_scope_symbol_table(lexeme, attribute):
            self._fail_switch(True)"""  # TODO: is deprecated?

    """def generate_llvm(self) -> str:

        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}

        ret = ""

        # lexeme = self._declarator.value
        ret += "%{0} = alloca {1}, align {2}\n".format(lexeme,
                                                       self._base_type.llvm_type,
                                                       self._base_type.llvm_alignment)
        if self._rhs is not None:
            ret += self._rhs.generate_llvm()
            ret += 'store {0} %{1}, {2}* %{3}\n'.format(self._base_type.llvm_type,
                                                       self.register_index,
                                                       self._base_type.llvm_type,
                                                       lexeme)
        return ret"""

    def handle_semantics(self):
        pass

    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes):
        attribute.type_spec = self._base_type
        super().add_to_scope_symbol_table(lexeme, attribute)
