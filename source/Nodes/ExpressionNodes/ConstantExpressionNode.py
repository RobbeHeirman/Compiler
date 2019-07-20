"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import struct

import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import type_specifier


class ConstantExpressionNode(ExpressionNode.ExpressionNode):

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self.constant = ctx.getText()
        self.l_value = False  # Constant's are always r value's

    @property
    def label(self) -> str:
        ret = super().label
        ret += "Constant: "
        ret += "{0}\n".format(self.constant)
        return ret

    @property
    def llvm_constant(self) -> str:
        if self._type_stack[0] is type_specifier.TypeSpecifier.CHAR:
            return str(ord(str(self.constant)[1]))

        elif self._type_stack[0] is type_specifier.TypeSpecifier.FLOAT:
            constant = float(self.constant)
            constant = struct.unpack('f', struct.pack('f', constant))[0]
            constant = hex(struct.unpack('Q', struct.pack('d', constant))[0])
            return constant

        return str(self.constant)

    def generate_llvm(self, store_reg: str = None) -> str:
        # Part of commenting.
        return_string = self.indent_string() + ";... {0}\n".format(self.constant)
        write_register = store_reg
        if not store_reg:
            self.increment_register_index()
            return_string += LlvmCode.llvm_allocate_instruction(str(self.register_index), self._type_stack,
                                                                self.indent_string())
            write_register = self.register_index

        return_string += LlvmCode.llvm_store_instruction_c(self._type_stack, self.llvm_constant, self._type_stack,
                                                           str(write_register), self.indent_string())

        return return_string

    def is_constant(self):
        return True
