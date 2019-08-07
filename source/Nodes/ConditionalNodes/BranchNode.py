"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.AbstractNode import AbstractNode


class BranchNode(AbstractNode):
    label = "Branch"

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._br_index = 0

    def assign_branch_index(self) -> int:
        ret = self._br_index
        self._br_index += 1
        return ret
