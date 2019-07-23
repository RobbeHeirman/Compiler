"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import struct

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode

import LlvmCode
import type_specifier


class ConstantExpressionNode(ExpressionNode.ExpressionNode):

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self.constant: str = ctx.getText()
        self.l_value: bool = False  # Constant's are always r value's

    def __str__(self):
        return self.constant

    # AST-visuals
    # ==================================================================================================================
    @property
    def label(self) -> str:
        ret = super().label
        ret += "Constant: "
        ret += "{0}\n".format(self.constant)
        return ret

    # Semantic-analysis
    # ==================================================================================================================
    def is_constant(self):
        return True

    # LLVM Code-Generation
    # ==================================================================================================================
    @property
    def llvm_value(self) -> str:
        if self._type_stack[0] == type_specifier.TypeSpecifier.CHAR:
            return str(ord(str(self.constant)[1]))

        elif self._type_stack[0] == type_specifier.TypeSpecifier.FLOAT:
            constant = float(self.constant)
            constant = struct.unpack('f', struct.pack('f', constant))[0]
            constant = hex(struct.unpack('Q', struct.pack('d', constant))[0])
            return constant

        return str(self.constant)

    def generate_llvm_store(self, store_addr: str) -> str:
        """
        Stores the constant directly in to given addr
        :param store_addr:
        :return:
        """

        return LlvmCode.llvm_store_instruction_c(self.llvm_value, self._type_stack, str(store_addr),
                                                 self._type_stack, self.code_indent_string())
