"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import Union

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


import messages
import type_specifier

from constants import MIPS_REGISTER_SIZE


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    # TypeAnnotations
    id: str
    l_value: bool

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self.id = ctx.getText()

        self.l_value = True  # As it's base form an identifier is an Lvalue
        self.code_l_value = True
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

    def is_read_only(self):
        attr = self.get_attribute(self.id)
        return attr.is_const

    # LLVM Code generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        ret = self.code_indent_string() + ";{0}\n".format(self)
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

        if not stack or stack[-1] != type_specifier.TypeSpecifier.FUNCTION \
                or stack[-1] != type_specifier.TypeSpecifier.ARRAY:
            ret_str += f'{self.code_indent_string()}lw ${reg}, {attribute.mips_stack_address}($sp)\n'

        if stack:
            self._type_modifier_node.reset_used_switches()

        while stack:
            element = stack.pop()

            # Need to find the value at address.
            if element == type_specifier.TypeSpecifier.POINTER:
                ret_str += f'{self.code_indent_string()}lw ${reg}, (${reg})\n'

            # Need to load in the address of where to find the val
            elif element == type_specifier.TypeSpecifier.ADDRESS:
                ret_str += f'{self.code_indent_string()}addiu ${reg}, $sp, {attribute.mips_stack_address}\n'

            elif element == type_specifier.TypeSpecifier.FUNCTION:

                # Set up the argument's in both register and on stack
                param_node = self._get_param_node()
                ret_str += param_node.mips_load_arguments(reg)

                # We need to save $ra
                ret_str += f'{self.code_indent_string()}subiu $sp, $sp, {MIPS_REGISTER_SIZE * 3} # Making room for link\n'
                ret_str += f'{self.code_indent_string()}sw $ra, ($sp) # Storing link\n'

                for i, reg in enumerate(self.mips_registers_in_use()):
                    ret_str += f'{self.code_indent_string()}sw ${reg}, {(i + 1) * MIPS_REGISTER_SIZE}($sp)\n'

                ret_str += f'{self.code_indent_string()}jal .{self.id}\n'

                # Free up stack that we used for arguments
                ret_str += param_node.mips_free_stack_of_arguments()
                # Restore link
                ret_str += f'{self.code_indent_string()}lw $ra, ($sp) # Restoring link\n'

                for i, reg in enumerate(self.mips_registers_in_use()):
                    ret_str += f'{self.code_indent_string()}lw ${reg}, {(i + 1) * MIPS_REGISTER_SIZE}($sp)\n'

                ret_str += f'{self.code_indent_string()}addiu $sp, $sp, {MIPS_REGISTER_SIZE * 3}\n'
                # move the return value in to assigned register
                ret_str += f'{self.code_indent_string()}move ${reg}, $v0\n'

            elif element == type_specifier.TypeSpecifier.ARRAY:
                arr_node = self._type_modifier_node.get_bottom_arr()

                # Calculate address
                extr_addr = self._parent_node.mips_register_reserve()
                muli_addr = self._parent_node.mips_register_reserve()

                ret_str += arr_node.expression_node.mips_store_in_register(extr_addr)
                ret_str += f'{self.code_indent_string()}li ${muli_addr}, {MIPS_REGISTER_SIZE}\n'
                ret_str += f'{self.code_indent_string()}mul ${extr_addr}, ${extr_addr}, ${muli_addr}\n'
                ret_str += f'{self.code_indent_string()}addu ${reg}, $sp, ${extr_addr}\n'
                ret_str += f'{self.code_indent_string()}lw ${reg}, {attribute.mips_stack_address}(${reg})\n'

                self._parent_node.mips_register_free(extr_addr)
                self._parent_node.mips_register_free(muli_addr)

        return ret_str

    def mips_store_address_in_reg(self, target_reg):

        attr = self._parent_node.get_attribute(self.id)
        number_on_stack = attr.mips_stack_address
        stack = self._generate_type_operator_stack()
        ret = f'{self.code_indent_string()}addu  ${target_reg}, $sp, {number_on_stack} \n'
        while stack:

            element = stack.pop()

            if element == type_specifier.TypeSpecifier.POINTER:
                ret += f'{self.code_indent_string()}lw ${target_reg}, (${target_reg})\n'

            elif element == type_specifier.TypeSpecifier.ARRAY:
                arr_node = self._type_modifier_node.get_bottom_arr()

                extr_addr = self._parent_node.mips_register_reserve()
                muli_addr = self._parent_node.mips_register_reserve()

                ret += arr_node.expression_node.mips_store_in_register(extr_addr)
                ret += f'{self.code_indent_string()}li ${muli_addr}, {MIPS_REGISTER_SIZE}\n'
                ret += f'{self.code_indent_string()}mul ${extr_addr}, ${extr_addr}, ${muli_addr}\n'
                ret += f'{self.code_indent_string()}addu ${target_reg}, $sp, ${extr_addr}\n'
                ret += f'{self.code_indent_string()}addu ${target_reg}, ${target_reg}, {number_on_stack}\n'

                self._parent_node.mips_register_free(extr_addr)
                self._parent_node.mips_register_free(muli_addr)

        return ret
