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
        printf_attr.llvm_name = var_id

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
        scanf_attr.llvm_name = var_id
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
        ret += f'{self.code_indent_string()}move $t2, $zero # We will use this to count arguments used.\n\n'

        # Start printf
        ret += f'{self.code_indent_string()}.start_printf:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}lw $a0, ($t0)# Load char at address\n'
        ret += f'{self.code_indent_string()}beqz $a0 .end_printf # 0 is the null terminator char\n'
        ret += f'{self.code_indent_string()}beq $a0, 37 .argument_print # ascii 37 = %\n\n'

        # No special chars
        ret += self.mips_comment("Default behaviour", c_comment)
        ret += f'{self.code_indent_string()}li $v0, 11 # Code for printing chars\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}addiu $t1, $t1, 1\n'
        ret += f'{self.code_indent_string()}addiu $t0, $t0, 4 # next word\n'
        ret += f'{self.code_indent_string()}b .start_printf\n\n'

        # % char found
        ret += f'{self.code_indent_string()}.argument_print: # Handling formatted string args\n'
        self.increase_code_indent()

        # Load the correct argument in place, first 2 will be placed in registers
        ret += f'{self.code_indent_string()} beq $t2, 0 .first_arg\n'
        ret += f'{self.code_indent_string()} beq $t2, 1 .second_arg\n'
        ret += f'{self.code_indent_string()} beq $t2, 2 .third_arg\n\n'

        # Load from stack
        ret += self.mips_comment("Load from stack if past argument range", c_comment)
        ret += f'{self.code_indent_string()}subi $t3, $t3, 3\n'
        ret += f'{self.code_indent_string()}mul $t3, $t4, 4\n'
        ret += f'{self.code_indent_string()}add $t3, $t4, $sp\n'
        ret += f'{self.code_indent_string()}lw $a0 ($t4)\n'
        ret += f'{self.code_indent_string()}b .type_control\n\n'

        # Load from $a1
        ret += f'{self.code_indent_string()}.first_arg:\n'
        self.increase_code_indent()
        ret += f"{self.code_indent_string()}move $a0, $a1\n"
        ret += f'{self.code_indent_string()}b .type_control\n\n'
        self.decrease_code_indent()

        # load from $a2
        ret += f'{self.code_indent_string()}.second_arg:\n'
        self.increase_code_indent()
        ret += f"{self.code_indent_string()}move $a0, $a2\n"
        ret += f'{self.code_indent_string()}b .type_control\n\n'
        self.decrease_code_indent()

        # load from $a3
        ret += f'{self.code_indent_string()}.third_arg:\n'
        self.increase_code_indent()
        ret += f"{self.code_indent_string()}move $a0, $a3\n\n"
        self.decrease_code_indent()
        self.decrease_code_indent()

        # type control
        ret += self.mips_comment("Load in the code based on type", c_comment)
        ret += f'{self.code_indent_string()}.type_control:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}addiu $t0, $t0, 4\n'
        ret += f'{self.code_indent_string()}lw $t3, ($t0)\n'
        ret += f'{self.code_indent_string()}beq $t3, 100 .print_int #104 is a "d"\n'
        ret += f'{self.code_indent_string()}beq $t3, 105, .print_int #111 is a "i"\n'
        ret += f'{self.code_indent_string()}beq $t3, 115, .print_char_string #123 is a s\n'
        ret += f'{self.code_indent_string()}beq $t3, 99 .print_char\n\n'

        # Not a valid code we just ignore the statement
        ret += f'{self.code_indent_string()}li $a0, 37 # We just going to print the invalid code\n'
        ret += f'{self.code_indent_string()}li $v0, 11\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}lw $a0, ($t0)\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}addiu $t1, $t1, 1\n'
        ret += f'{self.code_indent_string()}b .start_printf\n\n'

        # For integers
        ret += f'{self.code_indent_string()}.print_int:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}li $v0 1\n'
        ret += f'{self.code_indent_string()}b .print_code\n\n'
        self.decrease_code_indent()

        # For chars
        ret += f'{self.code_indent_string()}.print_char:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}li $v0 11\n'
        ret += f'{self.code_indent_string()}b .print_code\n\n'
        self.decrease_code_indent()

        # For strings
        ret += f'{self.code_indent_string()}.print_char_string:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}li $v0 4\n'
        ret += f'{self.code_indent_string()}b .print_code\n\n'
        self.decrease_code_indent()
        self.decrease_code_indent()
        # Print code
        ret += f'{self.code_indent_string()}.print_code:\n'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}addiu $t2, $t2 1\n'
        ret += f'{self.code_indent_string()}addiu $t0, $t0, 4\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}b .start_printf\n\n'
        self.decrease_code_indent()

        # End of code
        self.decrease_code_indent()
        ret += f'{self.code_indent_string()}.end_printf:'
        self.increase_code_indent()
        ret += f'{self.code_indent_string()}move $v0, $t1\n'
        ret += f'{self.code_indent_string()}jr $ra\n\n'
        self.decrease_code_indent()
        # scanf
        ret += '\n'
        ret += '.scanf:\n'
        ret += f'{self.code_indent_string()}li $v0, 12\n'
        ret += f'{self.code_indent_string()}syscall\n'
        ret += f'{self.code_indent_string()}sw $v0 ($a0)\n'
        self.decrease_code_indent()
        return ret
