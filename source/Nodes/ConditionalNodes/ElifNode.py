"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.ConditionalNodes import IfNode


class ElseIfNode(IfNode.IfNode):
    label = "else if"
