"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from Nodes.ExpressionNodes.RHSNode import RHSNode
from Nodes.ExpressionNodes.IdNode import IdNode
from Nodes.ExpressionNodes.ConstantNode import ConstantNode
from Nodes.DeclarationNodes.DeclaratorNode import DeclaratorNode
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import TypeSpecifier
from SymbolTable import Attributes


class DeclarationNode(ExpressionNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _lexeme: str
    _declarator_list: DeclaratorNode
    label = "Declaration"

    def __init__(self, parent_node: ExpressionNode):
        super().__init__(parent_node)

        self._declarator = None
        self._rhs = None
        self._id = None
        self._base_type = None

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
        self._declarator = child
        # self._id = child.value
        # self._declare_variable(child)

    def _add_rhs(self, child):
        self._rhs = child

    def _add_base_type(self, child: BaseTypeNode):
        self._base_type = child.value

    _add_overload_map = {
        DeclaratorNode: _add_declarator,
        ConstantNode: _add_rhs,
        IdNode: _add_rhs,
        RHSNode: _add_rhs,
        BaseTypeNode: _add_base_type,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode._add_overload_map[type(child)](self, child)
        super().add_child(child)

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

    def generate_llvm(self) -> str:
        """
        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}
        :return: the generated string
        """
        ret = ""

        # lexeme = self._declarator.value
        """ret += "%{0} = alloca {1}, align {2}\n".format(lexeme,
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
