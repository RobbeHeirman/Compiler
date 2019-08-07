"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.AbstractNode import AbstractNode


class BranchNode(AbstractNode):
    label = "Branch"
