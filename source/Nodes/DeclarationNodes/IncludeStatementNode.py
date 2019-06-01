"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.LeafNode import LeafNode


class IncludeStatementNode(LeafNode):
    label = "include \\n stdio.h"

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)

    def generate_llvm(self):
        return "declare i32 @printf(i8*, ...)\ndeclare i32 @scanf(i8*, ...)\n"
