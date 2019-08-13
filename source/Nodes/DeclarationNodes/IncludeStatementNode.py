"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

import Attributes
import messages
import type_specifier
from Nodes.AbstractNodes import AbstractNode


class IncludeStatementNode(AbstractNode.AbstractNode):
    label = "include \\n stdio.h"

    def __init__(self, parent_node, ctx: ParserRuleContext):
        super().__init__(parent_node, ctx)

    def semantic_analysis(self, messenger: messages.MessageGenerator):
        """
        add printf and scanf to the symbol table
        :param messenger:
        :return:
        """

        # printf
        var_id = "printf"
        ret_type = type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.INT)
        signature = [
            [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.CHAR),
             type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER)],

            [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.ANY)]
        ]

        func_type = type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.FUNCTION)
        func_type.function_signature = signature

        type_stack = [ret_type, func_type]

        printf_attr = Attributes.Attributes(type_stack, 0, 0)

        self._parent_node.add_to_scope_symbol_table(var_id, printf_attr)

        # scanf
        var_id = "scanf"
        ret_type = type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.INT)
        signature = [
            [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.CHAR),
             type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER)],

            [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.ANY)]
        ]
        func_type = type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.FUNCTION)
        func_type.function_signature = signature
        type_stack = [ret_type, func_type]
        scanf_attr = Attributes.Attributes(type_stack, 0, 0)
        self._parent_node.add_to_scope_symbol_table(var_id, scanf_attr)

        return True

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        return "declare i32 @printf(i8*, ...)\ndeclare i32 @scanf(i8*, ...)\n\n"

    # Mips Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        """
        We need to write printf in mips
        :param c_comment:
        :return:
        """

        # Start with a label
        ret = '.printf:\n'
        self.increase_code_indent()

        # We need to save our base address as prep
        ret += f'{self.code_indent_string()}move $t0, $a0 # Saving the base address\n'
        ret += f'{self.code_indent_string()}move $t1, $zero # Setting up counter for ret val\n'

        ret += f'{self.code_indent_string()}.start_printf:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}lw $a0, ($t0)\n # Load char at address\n'
        ret += f'{self.code_indent_string()}beqz $a0 .end_printf # 0 is the null terminator char\n'
        ret += f'{self.code_indent_string()}li $v0, 11 # Code for printing chars\n'
        ret += f'{self.code_indent_string()}syscall\n'

        ret += f'{self.code_indent_string()}addiu $t1, $t1, 1\n'
        ret += f'{self.code_indent_string()}addiu $t0, $t0, 4 # next word\n'
        ret += f'{self.code_indent_string()}b .start_printf\n'

        self.decrease_code_indent()
        ret += f'{self.code_indent_string()}.end_printf:\n'
        ret += f'{self.code_indent_string()}move $v0, $t1\n'
        ret += f'{self.code_indent_string()}jr $ra\n'

        # scanf
        ret += '\n'
        ret += '.scanf:\n'
        ret += f'{self.code_indent_string()}li $v0, 12\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}sw $v0 ($a0)\n'

        return ret
