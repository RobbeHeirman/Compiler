"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from source.Nodes.ConstantNode import ConstantNode
from source.Nodes.DeclaratorNode import DeclaratorNode
from source.Nodes.AbstractNode import AbstractNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.Specifiers import TypeSpecifier
from source.SymbolTable import Attributes


class DeclarationNode(ExpressionNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _lexeme: str
    _declarator_list: DeclaratorNode
    label = "Declaration"

    def __init__(self, parent_node: ExpressionNode):
        super().__init__(parent_node)

        self._base_type = None
        self._declarator = None
        self._rhs = None
        self._id = None

    @property
    def id(self):
        return self._id

    def _add_declarator(self, child: DeclaratorNode):
        self._declarator = child
        self._id = child.value
        # self._declare_variable(child)

    def _add_rhs(self, child):
        self._rhs = child

    _add_overload_map = {
        DeclaratorNode: _add_declarator,
        ConstantNode: _add_rhs,
        AbstractNode: None
    }

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """
        DeclarationNode._add_overload_map[type(child)](self, child)
        super().add_child(child)

    def declare_variable(self, base_type: TypeSpecifier):

        self._base_type = base_type
        node = self._children[0]
        filename = node.filename
        line = node.line
        column = node.column
        type_spec = self._base_type
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

        lexeme = self._declarator.value
        ret += "%{0} = alloca {1}, align {2}\n".format(lexeme,
                                                       self._base_type.llvm_type,
                                                       self._base_type.llvm_alignment)
        if self._rhs is not None:
            ret += 'store {0} {1}, {2}* %{3}'.format(self._base_type.llvm_type,
                                                     self._rhs.llvm_code_value(),
                                                     self._base_type.llvm_type,
                                                     lexeme)
        return ret

    def handle_semantics(self):
        pass
