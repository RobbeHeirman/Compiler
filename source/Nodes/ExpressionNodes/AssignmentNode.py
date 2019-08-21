"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from antlr4 import ParserRuleContext
import Nodes.ExpressionNodes.BinaryExpressionNode as BinaryExpressionNode
from Nodes.ExpressionNodes import ConstantExpressionNode


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

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis for assignments only extend's other binary operator's that the left side needs to be an
        LValue.
        :param messenger:
        :return:
        """
        if not super().semantic_analysis(messenger):
            return False

        if not self._left_expression.l_value:
            messenger.error_expected_l_value(self.line, self.column)

        if self._left_expression.is_read_only():
            messenger.error_is_read_only(self.line, self.column, self._left_expression.name())
            return False

        return True

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment=True) -> str:

        ret = self.llvm_comment(f'{self._left_expression} = {self._right_expression} ', c_comment)
        ret += self._left_expression.llvm_load(True)
        ret += self._right_expression.llvm_load()
        ret += self.code_indent_string() + f'store {self.llvm_type_string()} {self._right_expression.llvm_value},'
        ret += f' {self.llvm_type_string()}* {self._left_expression.llvm_value}\n'

        return ret

    @property
    def llvm_value(self) -> str:
        return self._left_expression.llvm_value

    # Mips Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        """
        Generates the mips code
        :param c_comment:
        :return:
        """
        addr1 = self.mips_register_reserve()

        ret = self.mips_comment(f'{self._left_expression} = {self._right_expression} ', c_comment)
        ret += self._left_expression.mips_store_address_in_reg(addr1)

        addr2 = self.mips_register_reserve()
        ret += self._right_expression.mips_store_in_register(addr2)
        ret += f'{self.code_indent_string()}sw, ${addr2}, (${addr1})\n'
        self.mips_register_free(addr1)
        self.mips_register_free(addr2)
        return ret
