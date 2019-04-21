"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod

from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Nodes.AbstractNodes.LeafNode import LeafNode


class RHSLeafNode(LeafNode, ABC):
    _parent_node: ExpressionNode

    def __init__(self, parent_node: ExpressionNode, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

    def generate_llvm(self):
        self.increment_register_index()
        return "%{0} = load {1}* {2}\n".format(self.register_index, self._parent_node.base_type.llvm_type,
                                             self.llvm_code_value())

    @abstractmethod
    def llvm_type(self):
        pass

    @abstractmethod
    def llvm_code_value(self):
        pass
