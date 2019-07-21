"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import messages
import type_specifier


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
    def generate_llvm(self):

        self.increment_register_index()

        if self._is_function_call():
            print("llvm for a function call")
            remember_reg = self.register_index

        else:
            ret = self.code_indent_string() + ";... {0}\n".format(self.id)
            ret += LlvmCode.llvm_load_instruction(self.id, self.type_stack, str(self.register_index), self.type_stack,
                                                  self.is_in_global_table(self.id), self.code_indent_string())

        return ret

    def _is_function_call(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        return False

    def _get_param_node(self):
        return self._type_modifier_node.get_param_node()
