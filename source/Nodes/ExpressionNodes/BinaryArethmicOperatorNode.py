"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum

import type_specifier
from Nodes.ExpressionNodes.BinaryExpressionNode import BinaryExpressionNode
from Nodes.ExpressionNodes.ConstantExpressionNode import ConstantExpressionNode


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

    @property
    def mips_op_code(self):
        _mips_op_code = {
            self.PLUS: "add",
            self.MINUS: "sub",
            self.MULTIPLY: "mul",
            self.DIVIDE: "div"
        }
        return _mips_op_code.get(self)


class BinaryArethmicOperatorNode(BinaryExpressionNode):

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._operator = Operator(ctx.getChild(1).getText())

        self._ctx = ctx

    def __str__(self):
        return f'{self._left_expression} {self._operator.value} {self._right_expression}'

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return self._operator.value

    # Semantic analysis
    # ==================================================================================================================
    def constant_folding(self):

        super().constant_folding()

        if isinstance(self._left_expression, ConstantExpressionNode) and \
                isinstance(self._right_expression, ConstantExpressionNode):

            val1 = self._left_expression.constant
            val2 = self._right_expression.constant

            type = self._left_expression.type_stack[-1]
            spec = None
            if type == type_specifier.TypeSpecifier.INT or type == type_specifier.TypeSpecifier.POINTER:
                val1 = int(val1)
                val2 = int(val2)
                spec = type_specifier.TypeSpecifier.INT
            elif type == type_specifier.TypeSpecifier.FLOAT:
                val1 = float(val1)
                val2 = float(val2)
                spec = type_specifier.TypeSpecifier.FLOAT
            elif type == type_specifier.TypeSpecifier.CHAR:
                val1 = ord(val1)
                val2 = ord(val2)
                spec = type_specifier.TypeSpecifier.CHAR
            res_val = 0
            if self._operator == Operator.PLUS:
                res_val = val1 + val2

            elif self._operator == Operator.MINUS:
                res_val = val1 - val2

            elif self._operator == Operator.MULTIPLY:
                res_val = val1 * val2

            elif self._operator == Operator.DIVIDE:
                res_val = val1 / val2

            node = ConstantExpressionNode(self._parent_node, self._ctx)
            node.type_stack_ref().append(type_specifier.TypeSpecifier(spec))
            node.constant = str(res_val)
            index = self._parent_node.get_child_index(self)
            self._parent_node.remove_child(self)
            self._parent_node.add_child(node, index)

    # LLVM Code
    # ==================================================================================================================

    def llvm_load(self, is_l_val: bool = False):
        ret = self._left_expression.llvm_load()
        ret += self._right_expression.llvm_load()

        self.increment_register_index()
        self._place_of_value = self.register_index

        ret += f'{self.code_indent_string()}{self.llvm_value} = {self._operator.llvm_op_code} {self.llvm_type_string()}'
        ret += f' {self._left_expression.llvm_value}, {self._right_expression.llvm_value}\n'

        return ret

    # MIPS Code
    # ==================================================================================================================
    def mips_store_in_register(self, reg: str):
        reg_1 = self.mips_register_reserve()
        ret = self._left_expression.mips_store_in_register(reg_1)
        reg_2 = self.mips_register_reserve()
        ret += self._right_expression.mips_store_in_register(reg_2)
        ret += f'{self.code_indent_string()}{self._operator.mips_op_code} ${reg}, ${reg_1}, ${reg_2}\n'

        self.mips_register_free(reg_1)
        self.mips_register_free(reg_2)

        return ret
