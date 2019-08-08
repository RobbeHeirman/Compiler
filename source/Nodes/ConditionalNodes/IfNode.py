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
        ret += self._condition_node.llvm_load(None, False)
        ret += f'{self.code_indent_string()}br i1 {self._condition_node.llvm_value}, label %{branch_to_true}'
        ret += f', label %{branch_to_false}\n\n'

        # Code when expression is True
        ret += f'{self.code_indent_string()}{branch_to_true}:\n'
        self.increase_code_indent()
        ret += self._statements_node.generate_llvm(c_comment)

        # Jump to end of branch block
        ret += f'{self.code_indent_string()}br label %{branch_to_end}\n\n'
        self.decrease_code_indent()

        return ret
