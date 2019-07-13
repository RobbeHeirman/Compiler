"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.AbstractNode import AbstractNode


class StatementsNode(AbstractNode):
    label = "Statements"

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)
