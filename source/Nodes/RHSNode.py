"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod

from antlr4 import ParserRuleContext

from source.Nodes.LeafNode import LeafNode


class RHSNode(LeafNode, ABC):

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

    @abstractmethod
    def llvm_code_value(self):
        pass
