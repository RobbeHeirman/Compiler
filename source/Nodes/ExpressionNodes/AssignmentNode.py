"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from antlr4 import ParserRuleContext
import Nodes.ExpressionNodes.BinaryExpressionNode as BinaryExpressionNode


class AssignmentNode(BinaryExpressionNode.BinaryExpressionNode):

    _BASE_LABEL = "="

    # Build ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx: ParserRuleContext):
        super().__init__(parent_node, ctx)

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return self._BASE_LABEL

    # def _find_id(self):
    #     self._id = self._lhs_node.find_id()
    #
    # def generate_llvm(self, c_comment: bool) -> str:
    #
    #     ret = self._children[0].generate_llvm(bool)
    #     ret += 'store {0} %{1}, {2}* %{3}\n'.format(self._base_type.llvm_type,
    #                                                 self.register_index,
    #                                                 self._base_type.llvm_type,
    #                                                 self._id)
    #     return ret

    @property
    def llvm_value(self) -> str:
        return ""
