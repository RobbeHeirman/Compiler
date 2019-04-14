"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.ExpressionNode import ExpressionNode


class AssignmentNode(ExpressionNode):

    label = "\"=\""

    def __init__(self, parent_node):
        super().__init__(parent_node)

    def resolve_expression(self):
        pass


    def generate_llvm(self):
        return ""
