"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode


class RHSParamListNode(NonLeafNode):

    @property
    def label(self):
        return "RHS Param list"
