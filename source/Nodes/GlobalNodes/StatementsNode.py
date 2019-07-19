"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.AbstractNode import AbstractNode
import Nodes.FunctionNodes.FuncDefNode


class StatementsNode(AbstractNode):
    label = "Statements"

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

    def get_return_type(self):
        self._parent_node: Nodes.FunctionNodes.FuncDefNode.FuncDefNode
        return self._parent_node.get_return_type()
