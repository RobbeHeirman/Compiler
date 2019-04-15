"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from source.Nodes.RHSNode import RHSNode


class IdNode(RHSNode):

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

    @property
    def label(self):
        return str(self._value)

    def is_declared(self)->bool:
        if not self._parent_node.is_in_table(self._value):
            print("Not in symbol table") #TODO semantic error
            return False
        return True

    def llvm_code_value(self):
        return str(self._value)