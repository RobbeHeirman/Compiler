"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4.tree.Tree import TerminalNodeImpl

from source.Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from source.Nodes.AbstractNodes.ScopedNode import ScopedNode
from source.Specifiers import DeclType, TypeSpecifier
from source.SymbolTable import Attributes
from source.messages import redeclared_diff_symbol, note_prev_decl


class FuncDefNode(ScopedNode):
    _id: str
    _parent_node: ExpressionNode

    def __init__(self, parent_node: ExpressionNode, id_l: str, filename: str, ctx: TerminalNodeImpl):
        super().__init__(parent_node)

        self._id = id_l
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
        return '"func def: {0}"'.format(self._id)
