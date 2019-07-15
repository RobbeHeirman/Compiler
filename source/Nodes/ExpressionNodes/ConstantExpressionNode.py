"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import struct

import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
from Specifiers import TypeSpecifier


class ConstantExpressionNode(ExpressionNode.ExpressionNode):

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)

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
        if self._type_stack[0] is TypeSpecifier.CHAR:
            return str(ord(str(self.constant)[1]))

        elif self._type_stack[0] is TypeSpecifier.FLOAT:
            constant = float(self.constant)
            constant = struct.unpack('f', struct.pack('f', constant))[0]
            constant = hex(struct.unpack('Q', struct.pack('d', constant))[0])
            return constant

        return str(self.constant)

    def add_base_type(self, base_type):
        self._type_stack.append(base_type)

    def generate_llvm(self) -> str:
        self.increment_register_index()
        ret = self.indent_string() + ";... {0}\n".format(self.constant)
        ret += LlvmCode.llvm_allocate_instruction(str(self.register_index), self._type_stack, self.indent_string())
        ret += LlvmCode.llvm_store_instruction_c(self._type_stack, self.llvm_constant,
                                                 self._type_stack, str(self.register_index), self.indent_string())
        prev_index = self.register_index
        self.increment_register_index()
        ret += LlvmCode.llvm_load_instruction(str(prev_index), self._type_stack, str(self.register_index),
                                              self._type_stack, self.indent_string())

        return ret

    def is_constant(self):
        return True
