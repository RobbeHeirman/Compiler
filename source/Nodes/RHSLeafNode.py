"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod

from antlr4 import ParserRuleContext

from source.Nodes.LeafNode import LeafNode


class RHSLeafNode(LeafNode, ABC):

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

    def generate_llvm(self):
        self.increment_register_index()
        return "%{0} load {1}* {2}\n".format(self.register_index, self.llvm_type(), self.llvm_code_value())

    @abstractmethod
    def llvm_type(self):
        pass

    @abstractmethod
    def llvm_code_value(self):
        pass
