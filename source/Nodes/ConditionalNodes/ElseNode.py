"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes import ScopedNode
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ConditionalNodes import BranchNode
from Nodes.GlobalNodes import StatementsNode


class ElseNode(ScopedNode.ScopedNode):
    label = "Else"
    _parent_node: BranchNode.BranchNode
    # Built ins
    # ==================================================================================================================

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._statements_node: StatementsNode.StatementsNode = None
        self.labels_needed = 1

    # AST Generation
    # ==================================================================================================================
    def add_child(self, child: "AbstractNode", index: int = None):
        if isinstance(child, StatementsNode.StatementsNode):
            self._statements_node = child

        super().add_child(child, index)

    def generate_llvm(self, c_comment: bool = True):
        nw_br_label = self._parent_node.assign_label()
        end_branch = self._parent_node.end_label()
        ret = self.code_indent_string() + nw_br_label + ":\n"
        ret += self._statements_node.generate_llvm(c_comment)

        if self._statements_node.has_return_node():
            self.decrease_code_indent()
            ret += "\n"
            return ret

        ret += f'{self.code_indent_string()}br label %{end_branch}\n\n'
        return ret
