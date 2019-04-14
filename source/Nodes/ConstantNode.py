"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.LeafNode import LeafNode


class ConstantNode(LeafNode):

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)

    @property
    def label(self):
        return "\"{0}\"".format(str(self._value))
