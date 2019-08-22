"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.ConditionalNodes.BreakNode import BreakNode
from Nodes.ConditionalNodes.WhileNode import WhileNode


class ContinueNode(BreakNode):
    label = "continue"

    def generate_llvm(self, c_comment: bool = True):
        node: WhileNode = self._parent_node.find_while_sw_node()
        self.increment_register_index()
        return f'{self.code_indent_string()}br label %{node.start_label}\n'

    def generate_mips(self, c_comment: bool = True):
        node: WhileNode = self._parent_node.find_while_sw_node()
        return f'{self.code_indent_string()}b {node.start_label}\n'
