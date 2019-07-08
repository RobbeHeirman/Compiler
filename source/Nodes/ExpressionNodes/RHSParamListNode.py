"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import Nodes.AbstractNodes.AbstractNode as AbstractNode


class RHSParamListNode(AbstractNode.AbstractNode):

    @property
    def label(self):
        return "RHS Param list"
