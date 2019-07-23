"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode

import LlvmCode
import messages


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    # TypeAnnotations
    id: str
    _l_value: bool

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self.id = ctx.getText()
        self._l_value = True  # As it's base form an identifier is an Lvalue

        self._temporal_reg_num: int = None

    def __str__(self):
        return self.id

    # AST visuals
    # ==================================================================================================================
    @property
    def label(self) -> str:

        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger: messages.MessageGenerator) -> bool:

        # First check if the id was declared
        if not self.is_in_table(self.id):
            messenger.error_undeclared_var(self.id, self._line, self._column)
            return False

        self._type_stack = self.get_attribute(self.id).operator_stack
        if not self._generate_type_modifier_stack(messenger):  # the modifiers applied in the expression

            return False
        return True

    # LLVM Code generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        self.increment_register_index()

        if self._is_function_call():
            print("llvm for a function call")

            # We pop off the function type since it's a call
            self._type_stack.pop()
            # This node will load all the value's in place
            param_node = self._get_param_node()
            ret = param_node.llvm_call_param_nodes()

            # This is the base register the functions will load from
            remember_reg = self.register_index

        else:
            ret = self.code_indent_string() + ";... {0}\n".format(self.id)
            ret += self.llvm_load()

        return ret

    def llvm_load(self) -> str:
        """
        Will load this variable into a register
        :return: a string that loaded the value of the var into the register
        """
        self.increment_register_index()
        self._temporal_reg_num = self.register_index

        if self._is_function_call():
            param_node = self._get_param_node()

            param_node.llvm_load_params()
            call_string = '('

            child_list: List[ExpressionNode] = param_node.get_children()
            call_string += ', '.join([child.llvm_value for child in child_list])
            call_string += ')'
            print(call_string)

            return f'%{self._temporal_reg_num} = call {self._type_stack[0].llvm_type} @{self.id}{call_string}\n'

        return LlvmCode.llvm_load_instruction(self.id, self.type_stack, str(self.register_index), self.type_stack,
                                              self.is_in_global_table(self.id), self.code_indent_string())

    def generate_llvm_store(self, addr: str):
        print("???")
        if self._is_function_call():
            print("llvm for a function call")

        ret = self.llvm_load()
        ret += LlvmCode.llvm_store_instruction(str(self.register_index), self._type_stack, addr, self._type_stack,
                                               self.code_indent_string())
        return ret

    def _is_function_call(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        return False

    def _get_param_node(self) -> ParamListNode.ParamListNode:
        return self._type_modifier_node.get_param_node()

    def llvm_value(self):
        return f'@{self._temporal_reg_num}' if self.is_in_global_table(self.id) else f'%{self._temporal_reg_num}'
