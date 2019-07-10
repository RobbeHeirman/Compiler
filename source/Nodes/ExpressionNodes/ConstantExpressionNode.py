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

    def __init__(self, parent_node, constant):
        super().__init__(parent_node)

        self.constant = constant

    @property
    def label(self) -> str:
        ret = super().label
        ret += "Constant: "
        ret += "{0}\n".format(self.constant)
        return ret

    @property
    def llvm_constant(self) -> str:
        if self.base_type is TypeSpecifier.CHAR:
            return str(ord(str(self.constant)[1]))
        elif self.base_type is TypeSpecifier.FLOAT:
            constant = float(self.constant)
            constant = struct.unpack('f', struct.pack('f', constant))[0]
            constant = hex(struct.unpack('Q', struct.pack('d', constant))[0])
            return constant

        return str(self.constant)

    def generate_llvm(self) -> str:
        self.increment_register_index()
        ret = self.indent_string() + ";... {0}\n".format(self.constant)
        ret += LlvmCode.llvm_allocate_instruction(str(self.register_index), self.base_type, [],
                                                  self.indent_string())

        ret += LlvmCode.llvm_store_instruction_c(self.base_type, self.llvm_constant, [],
                                                 self.base_type, str(self.register_index), [],
                                                 self.indent_string())
        prev_index = self.register_index
        self.increment_register_index()
        ret += LlvmCode.llvm_load_instruction(self.base_type, str(prev_index), [], self.base_type,
                                              str(self.register_index), [], self.indent_string())

        return ret

    def is_constant(self):
        return True
