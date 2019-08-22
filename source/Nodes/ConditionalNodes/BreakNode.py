"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ConditionalNodes.WhileNode import WhileNode


class BreakNode(AbstractNode):
    label = "break"

    # Semantic-analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger: messages.MessageGenerator):
        node = self._parent_node.find_while_sw_node()

        if not node:
            messenger.error_break_not_while(self.line, self.column)
            return False

        return True

    # LLVM-Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        node: WhileNode = self._parent_node.find_while_sw_node()
        self.increment_register_index()
        return f'{self.code_indent_string()}br label %{node.end_label}\n\n'

    # Mips-Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        grand_parent: WhileNode = self._parent_node.find_while_sw_node()
        return f'{self.code_indent_string()}b {grand_parent.end_label}\n\n'
