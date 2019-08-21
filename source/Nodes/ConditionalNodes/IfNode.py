"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ConditionalNodes import ElseNode
from Nodes.ExpressionNodes import ConditionNode


class IfNode(ElseNode.ElseNode):
    label = "if"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._condition_node: ConditionNode.ConditionNode = None
        self.labels_needed = 1

    # AST Generation
    # ==================================================================================================================
    def add_child(self, child: "AbstractNode", index: int = None):
        if isinstance(child, ConditionNode.ConditionNode):
            self._condition_node = child

        super().add_child(child, index)

    # LLVM Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        # Labels to jump to
        branch_to_true = self._parent_node.assign_label()
        branch_to_false = self._parent_node.next_label()
        branch_to_end = self._parent_node.end_label()

        # Check condition
        ret = self.llvm_comment(f'if {self._condition_node}', c_comment)
        ret += self._condition_node.llvm_load()
        ret += f'{self.code_indent_string()}br i1 {self._condition_node.llvm_value}, label %{branch_to_true}'
        ret += f', label %{branch_to_false}\n\n'

        # Code when expression is True
        ret += f'{self.code_indent_string()}{branch_to_true}:\n'
        self.increase_code_indent()
        ret += self._statements_node.generate_llvm(c_comment)

        if self._statements_node.has_return_node():
            self.decrease_code_indent()
            ret += "\n"
            return ret

        # Jump to end of branch block
        ret += f'{self.code_indent_string()}br label %{branch_to_end}\n\n'
        self.decrease_code_indent()

        return ret

    # Mips Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):

        branch_to_false = self._parent_node.next_label()
        branch_to_end = self._parent_node.mips_end_label()
        ret = self.mips_comment(f'if {self._condition_node}', c_comment)
        self.increase_code_indent()
        ret += self._condition_node.mips_store_in_register('t0')
        ret += f'{self.code_indent_string()}beqz $t0, {branch_to_false}\n\n'
        self.decrease_code_indent()

        ret += self.mips_comment("if true:", c_comment)
        self.increase_code_indent()
        ret += self._statements_node.generate_mips(c_comment)

        ret += f'{self.code_indent_string()}b {branch_to_end}\n\n'
        self.decrease_code_indent()
        return ret
