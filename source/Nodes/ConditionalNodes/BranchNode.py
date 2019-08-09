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
        self._br_index = 0
        return ret

    def llvm_end_branch_index(self) -> int:
        self._children: List[ElseNode]
        return sum([child.labels_needed for child in self._children])

    # Mips code generation
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        ret = super().generate_mips(c_comment)
        ret += f'{self.code_indent_string()}{self.mips_end_label()}:\n'
        self._br_index = 0
        return ret

    def mips_end_branch_index(self) -> int:
        return len(self._children) - 1

    def mips_end_label(self) -> str:
        return f'{self.branch_base_label}{self.mips_end_branch_index()}'

    # Meta code generation
    # ==================================================================================================================
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
        return f'{self.branch_base_label}{self.llvm_end_branch_index()}'
