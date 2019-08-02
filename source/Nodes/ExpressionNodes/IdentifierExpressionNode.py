"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import Union

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


import LlvmCode
import messages
import type_specifier

from constants import MIPS_REGISTER_SIZE


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
        self._place_of_value: Union[int, str] = self.id  # The register the current value of the identifier is placed

        self._is_global = False

    def __str__(self):
        return f'{self.id}{[child for child in self._type_stack]} Modified: ' \
            f'{[child for child in self._generate_type_operator_stack()]}'

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

        self._is_global = True if self.is_in_global_table(self.id) else False
        self._type_stack = self.get_attribute(self.id).operator_stack
        if not self._generate_secondary_types(messenger):  # the modifiers applied in the expression

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

        else:
            ret = self.code_indent_string() + ";... {0}\n".format(self.id)
            ret += self.llvm_load()

        return ret

    def generate_llvm_store(self, addr: str) -> str:
        """
        Tell the IDExpresionNode to store it's value to a certain address. This could be a temporal address
        or a register constructed by a declaration. The trick is to deduce the corresponding loads, calls and stores
        depending on the type Modifiers
        :param addr:  the address to store to
        :return: The generated store instruction string
        """
        ret = self.llvm_load()
        ret += LlvmCode.llvm_store_instruction(self._place_of_value, self._type_stack, addr, self._type_stack,
                                               self.code_indent_string())
        return ret

    def _is_function_call(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        return False

    @property
    def llvm_value(self):
        if not self._is_global:
            return f'%{self._place_of_value}'
        return f'@{self._place_of_value}'

    # Mips code
    # ==================================================================================================================
    def mips_store_in_register(self, reg: str) -> str:
        """
        Store the value of the identifier Expression in target register.
        We also need to take in account some operators are applied

        :param str reg: the target register
        :return str: A Mips Code string
        """

        # We need to find where the value of this variable is located
        attribute = self._parent_node.get_attribute(self.id)
        ret_str = ""
        stack = self._generate_type_operator_stack()
        if not stack or stack[-1] != type_specifier.TypeSpecifier.FUNCTION:

            ret_str += self.code_indent_string()
            if attribute.mips_is_register:
                ret_str += f"move ${reg}, ${attribute.mips_register}\n"
            else:
                ret_str += f'lw ${reg}, {attribute.mips_stack_address}($sp)\n'

        while stack:
            element = stack.pop()

            # Need to find the value at address.
            if element == type_specifier.TypeSpecifier.POINTER:
                ret_str += f'{self.code_indent_string()}lw ${reg}, (${reg})\n'

            # Need to load in the address of where to find the val
            elif element == type_specifier.TypeSpecifier.ADDRESS:
                ret_str += f'{self.code_indent_string()}addiu ${reg}, $sp, {attribute.mips_stack_address}\n'

            elif element == type_specifier.TypeSpecifier.FUNCTION:
                # We need to save $ra
                ret_str += f'{self.code_indent_string()}subiu $sp, $sp, {MIPS_REGISTER_SIZE} # Making room for link \n'
                ret_str += f'{self.code_indent_string()}sw $ra, ($sp) # Storing link\n'
                # Set up the argument's in both register and on stack
                param_node = self._get_param_node()
                ret_str += param_node.mips_load_arguments()
                ret_str += f'{self.code_indent_string()}jal .{self.id}\n'

                # Free up stack that we used for arguments
                ret_str += param_node.mips_free_stack_of_arguments()
                # Restore link
                ret_str += f'{self.code_indent_string()}lw $ra, ($sp) # Restoring link\n'
                ret_str += f'{self.code_indent_string()}addiu $sp, $sp, {MIPS_REGISTER_SIZE}\n'
                # move the return value in to assigned register
                ret_str += f'{self.code_indent_string()}move ${reg}, $v0\n'
        return ret_str
