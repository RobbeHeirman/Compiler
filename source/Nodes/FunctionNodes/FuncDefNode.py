"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4.tree.Tree import TerminalNodeImpl

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Nodes.AbstractNodes.ScopedNode import ScopedNode
from Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from Specifiers import DeclType, TypeSpecifier
from SymbolTable import Attributes
from messages import redeclared_diff_symbol, note_prev_decl


class FuncDefNode(ScopedNode):
    _id: str
    _parent_node: ExpressionNode

    def __init__(self, parent_node: ExpressionNode, id_l: str, ptr_count: int, filename: str, ctx: TerminalNodeImpl):
        super().__init__(parent_node)

        self._id = id_l
        self._ptr_count = ptr_count
        self._base_type = None
        self._base_type_node = None
        attr = Attributes(TypeSpecifier.DEFAULT, filename, ctx.getSymbol().line, ctx.getSymbol().column,
                          DeclType.FUNCTION)
        if self._parent_node.is_in_table(self._id):  # Declared in global scope?
            attr2 = self._parent_node.get_attribute(self._id)
            if attr2.decl_type != DeclType.FUNCTION:  # Should be a forward declaration
                self._fail_switch(True)
                redeclared_diff_symbol(self._id, attr)
                note_prev_decl(self._id, attr2)

    @property
    def label(self):
        ptr_label = "*" * self._ptr_count
        return 'Func def\nIdentifier: {0}\nReturn type {1}{2}'.format(self._id, self._base_type.value, ptr_label)

    def add_child(self, child):

        if isinstance(child, BaseTypeNode):
            self._base_type_node = child
            self._base_type = child.value
        super().add_child(child)

    def first_pass(self):

        self._base_type = self._base_type_node.value
        self.remove_child(self._base_type_node)
        self._base_type_node = None

        super().first_pass()
