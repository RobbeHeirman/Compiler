"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ConditionalNodes import ElseNode
from Nodes.ExpressionNodes import ConditionNode

class IfNode(ElseNode.ElseNode):
    label = "if"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._condition_node: ConditionNode.ConditionNode = None

    # AST Generation
    # ==================================================================================================================
    def add_child(self, child: "AbstractNode", index: int = None):
        if isinstance(child, ConditionNode.ConditionNode):
            self._condition_node = child

        super().add_child(child, index)
