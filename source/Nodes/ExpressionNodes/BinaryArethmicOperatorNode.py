"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum

from Nodes.ExpressionNodes.BinaryExpressionNode import BinaryExpressionNode


class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'

    @property
    def llvm_op_code(self):
        _llvm_op_code = {
            self.PLUS: "add",
            self.MINUS: "sub",
            self.MULTIPLY: "mul",
            self.DIVIDE: "sdiv"
        }

        return _llvm_op_code.get(self)


class BinaryArethmicOperatorNode(BinaryExpressionNode):

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._operator = Operator(ctx.getChild(1).getText())

    def __str__(self):
        return f'{self._left_expression} {self._operator.value} {self._right_expression}'

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return self._operator.value

    # LLVM Code
    # ==================================================================================================================

    def llvm_load(self, reg_load_from=None, is_l_val: bool = False):
        ret = self._left_expression.llvm_load(None, False)
        ret += self._right_expression.llvm_load(None, False)

        self.increment_register_index()
        self._place_of_value = self.register_index

        ret += f'{self.code_indent_string()}{self.llvm_value} = {self._operator.llvm_op_code} {self.llvm_type_string()}'
        ret += f' {self._left_expression.llvm_value}, {self._right_expression.llvm_value}\n'

        return ret
