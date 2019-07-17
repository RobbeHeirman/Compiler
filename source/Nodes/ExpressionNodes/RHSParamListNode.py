"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.FunctionNodes.ParamListNode as ParamListNode


class RHSParamListNode(ParamListNode.ParamListNode):

    @property
    def label(self):
        return "RHS Param list"
