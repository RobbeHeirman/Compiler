"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

import messages
from Nodes.ExpressionNodes.RHSLeafNode import RHSLeafNode
from Specifiers import TypeSpecifier
from SymbolTable import Attributes


class IdNode(RHSLeafNode):

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

        self.is_declared()

    @property
    def label(self):
        return str(self._value)

    def is_declared(self)->bool:
        if not self._parent_node.is_in_table(self._value):
            attr = Attributes(TypeSpecifier.DEFAULT, self._filename, self._line, self._column)
            messages.error_undeclared_var(self._value, attr)
            self._fail_switch(True)
            return False
        return True

    def llvm_code_value(self):
        return str(self._value)

    def llvm_type(self):

        attr = self._parent_node.get_attribute(self._value)
        typ = attr.type_spec
        return typ.llvm_type
