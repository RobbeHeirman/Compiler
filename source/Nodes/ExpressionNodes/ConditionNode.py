"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum

import type_specifier
from Nodes.ExpressionNodes.BinaryExpressionNode import BinaryExpressionNode


class ConditionalOperator(Enum):
    BIGGER = '>'
    SMALLER = '<'
    EQUALS = '=='

    @property
    def llvm_value(self):
        _LLVM_VAL_MAP = {
            self.BIGGER: 'sgt',
            self.SMALLER: 'slt',
            self.EQUALS: 'eq'
        }

        return _LLVM_VAL_MAP[self]


class ConditionNode(BinaryExpressionNode):

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx, operator):
        super().__init__(parent_node, ctx)

        self._type = ConditionalOperator(operator)

    def __str__(self):
        return f'{self._left_expression} {self._type.value} {self._right_expression}'

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return self._type.value

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger):
        if not super().semantic_analysis(messenger):
            return False

        self._type_stack = [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.BOOL)]
        return True

    # LLVM code generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        return self.llvm_load(None, False)

    def llvm_load(self, reg_load_from=None, is_l_val: bool = False):
        ret = self._left_expression.llvm_load(None, False)
        ret += self._right_expression.llvm_load(None, False)
        self.increment_register_index()
        self._place_of_value = self.register_index

        ret += f'{self.code_indent_string()}%{self.register_index} = icmp {self._type.llvm_value}'
        ret += f' {self._left_expression.llvm_type_string()} {self._left_expression.llvm_value},' \
            f' {self._right_expression.llvm_value}\n'

        return ret
