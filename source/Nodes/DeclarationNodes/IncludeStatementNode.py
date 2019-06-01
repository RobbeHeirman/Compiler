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

    def semantic_analysis(self):
        """
        Needs to set printf and scanf into symbol table
        :return:
        """

        # First of printf
        id = "printf"
        return True
