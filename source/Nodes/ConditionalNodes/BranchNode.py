"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, TYPE_CHECKING

from Nodes.AbstractNodes.AbstractNode import AbstractNode

if TYPE_CHECKING:
    from Nodes.ConditionalNodes.ElseNode import ElseNode


class BranchNode(AbstractNode):
    label = "Branch"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._br_index = 0

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        ret = super().generate_llvm(c_comment)
        ret += f'{self.code_indent_string()}{self.end_label()}:\n'
        return ret

    @property
    def branch_base_label(self):
        return f'{self._parent_node.code_function_base_label}_br'

    def assign_label(self) -> str:
        return f'{self.branch_base_label}{self.assign_branch_index()}'

    def assign_branch_index(self) -> int:
        ret = self._br_index
        self._br_index += 1
        return ret

    def next_label(self) -> str:
        return f'{self.branch_base_label}{self._br_index}'

    def end_label(self):
        return f'{self.branch_base_label}{self.end_branch_index()}'

    def end_branch_index(self) -> int:
        self._children: List[ElseNode]
        return sum([child.labels_needed for child in self._children])
