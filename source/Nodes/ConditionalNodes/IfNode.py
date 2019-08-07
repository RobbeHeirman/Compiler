"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes import ConditionNode
from Nodes.GlobalNodes import StatementsNode
from Specifiers import ConditionType


class IfNode(ScopedNode.ScopedNode):
    label = "if"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx: ConditionType):
        super().__init__(parent_node, ctx)

        self._statements_node: StatementsNode.StatementsNode = None
        self._condition_node: ConditionNode.ConditionNode = None

    # AST Generation
    # ==================================================================================================================
    def add_child(self, child: "AbstractNode", index: int = None):

        if isinstance(child, StatementsNode.StatementsNode):
            self._statements_node = child

        elif isinstance(child, ConditionNode.ConditionNode):
            self._condition_node = child

        super().add_child(child, index)
