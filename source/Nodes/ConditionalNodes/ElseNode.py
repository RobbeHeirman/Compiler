"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes import ScopedNode
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.GlobalNodes import StatementsNode


class ElseNode(ScopedNode.ScopedNode):
    label = "Else"

    # Built ins
    # ==================================================================================================================

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._statements_node: StatementsNode.StatementsNode = None

    # AST Generation
    # ==================================================================================================================
    def add_child(self, child: "AbstractNode", index: int = None):
        if isinstance(child, StatementsNode.StatementsNode):
            self._statements_node = child

        super().add_child(child, index)
