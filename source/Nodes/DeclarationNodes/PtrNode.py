"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.LeafNode import LeafNode


class PtrNode(LeafNode):
    label = "*"

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node, filename, ctx)
