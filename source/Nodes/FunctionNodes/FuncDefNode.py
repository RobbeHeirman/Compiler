"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.AbstractNodes.ScopedNode as ScopedNode
import Nodes.GlobalNodes.GlobalDeclarationNode as GlobalDeclarationNode
import Attributes
import type_specifier
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Nodes.GlobalNodes.StatementsNode

from constants import MIPS_REGISTER_SIZE


class FuncDefNode(GlobalDeclarationNode.GlobalDeclarationNode, ScopedNode.ScopedNode):
    # The Mips Register ref's. Used for comparing with mips register stack's
    _LAZY_MIPS_REGISTERS = tuple(f't{i}' for i in reversed(range(2, 10)))  # Using $t0, $t1 as temporal work address
    _PRESERVE_MIPS_REGISTERS = tuple(f's{i}' for i in reversed(range(8)))

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node: AbstractNode.AbstractNode, ctx):
        super().__init__(parent_node, ctx)
        self._param_list_node: ParamListNode.ParamListNode = None
        self._function_signature = []

        self._llvm_register_index = 0

        # We need a mechanism to keep track of the Mips Register's available
        self._lazy_mips_registers_available = list(self.__class__._LAZY_MIPS_REGISTERS)
        self._preserve_mips_registers_available = list(self.__class__._PRESERVE_MIPS_REGISTERS)
        self._mips_stack_pointer: int = 0

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return 'Func def\nIdentifier: {0}\nReturn type {1}'.format(self.id, [el.value for el in
                                                                             self._type_stack[:-1]])

    # AST-generation
    # ==================================================================================================================
    @property
    def base_type(self):
        return self._type_stack[0]

    @base_type.setter
    def base_type(self, tp):
        self._type_stack.append(tp)

    def add_child(self, child, index=None):

        if isinstance(child, Nodes.GlobalNodes.StatementsNode.StatementsNode):
            self._expression_node = child

        elif isinstance(child, ParamListNode.ParamListNode):
            self._param_list_node = child

        super().add_child(child, index)

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis of a function definition.
        1)The function and his signature needs to be added to the symbol
        Table of the upper scope.
        2) The parameters are declared variables belonging to the scope of this function.
        :return: If the semantic analysis is correct.
        """
        # Check if the children are playing nice

        if not self._param_list_node.semantic_analysis(messenger):
            return False

        # Applies all special types to the function definition
        self._generate_secondary_types(messenger)
        self._type_stack.append(type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.FUNCTION,
                                                             self._param_list_node.get_function_signature()))

        self._function_signature = self._param_list_node.get_function_signature()
        attribute = Attributes.AttributesGlobal(self._type_stack, self._line, self._column, True, self)

        attribute.function_signature = self._function_signature
        if not self._add_to_table(attribute, messenger):
            return False

        for child in self._children:
            if child is not self._param_list_node:
                if not child.semantic_analysis(messenger):
                    return False
        return True

    def get_return_type(self):
        return self._type_stack[:-1]

    # LLVM Code-Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        attr = self.get_attribute(self.id)
        attr.llvm_name = self.id
        function_signature = self._param_list_node.generate_llvm_function_signature()
        return_type = f'{"".join([child.llvm_type for child in self._type_stack[:-1]])} '
        ret = self.comment_code(c_comment, False)
        ret += f'{self.code_indent_string()} define {return_type} @{self.id}'
        ret += f'({function_signature}){{\n'
        self.increase_code_indent()

        # Read and store the parameters to their respective registers.
        ret += self._param_list_node.llvm_load_params()
        ret += self._param_list_node.llvm_store_params()

        # get a return reg up
        ret += f'{self.code_indent_string()}%.ret = alloca {return_type}\n'
        # We need to increment our register for each param
        self.increment_register_index(self._param_list_node.child_count())

        for child in self._children[1:]:
            ret += child.generate_llvm(c_comment)

        # if self._return_node is None:
        #     ret += self.indent_string() + "  ret {0} 0\n".format(self.base_type.llvm_type)

        # ret_type_str = "".join([c_type.llvm_type for c_type in self.get_return_type()])
        # ret += self.code_indent_string() + "ret {0} %{1}\n".format(ret_type_str, '0')

        # Return
        ret += f'{self.code_indent_string()}{self.return_label()}:\n'
        self.increase_code_indent()
        self.increment_register_index()
        ret += f'{self.code_indent_string()}%{self.register_index} = load {return_type}, {return_type}* %.ret\n'
        ret += f'{self.code_indent_string()} ret {return_type} %{self.register_index}\n'
        self.decrease_code_indent()
        ret += "}\n"
        self.decrease_code_indent()
        return ret

    @property
    def register_index(self) -> int:
        """
        the register index that is on top available.
        :return: int register index
        """
        return self._llvm_register_index

    def increment_register_index(self, amount: int = 1) -> None:
        """
        Increment the next available register index
        :param amount: int by amount we increase, 1 by default.
        """
        self._llvm_register_index += amount

    def return_label(self) -> str:
        return f'{self.id}_return'

    # MIPS Code-Generation
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True) -> str:
        """
        A Mips (sub) routine definition. Mips routines: Argument's in a0-a3, rest passed on the stack.
        Return value's in v0 and v1. Steps for a routine definition follows
        1) Label the routine
        2) Make room on the stack for local variables (Callee's stack frame)
        3) Notify the front end where the argument's can be found (in registers or on stack)
        4) Routine Body
        5) Make a return label. ReturnNodes will use those to jump to to return to the caller (at ra)

        :param bool c_comment: If False we don't write comments in code.
        :return string: A string of MipsCode. Generated of this function definition.
        """
        # 0 Starting comment's. = A pseudo code (a bit like C) that shows witch statement we are generating
        ret = '\n\n' + self.comment_code(c_comment)

        # 1 Label the start of the function. We add a . to prevent name clashes with compiler defined labels.
        ret += f'.{self.id}:\n'
        self.increase_code_indent()

        # 2 Make room on the stack for local variable's
        frame_size = self._expression_node.mips_stack_space_needed()

        # 3) Now we need to notify the front end where we can find (and where to store in case of subroutine call)
        #    Argument's. We let the parameter node handle that. It has more complete information about param's.
        #    We Allocate some memory for reg argument's on the stack.
        self._param_list_node.mips_assign_params_to_mem(frame_size)

        # Assign addresses to the declared variable's if available.
        self._expression_node.mips_assign_register()

        # Store the register's $s0 - $s7 to memory
        load_preserved_regs_from = self.mips_stack_pointer
        temp_ret = self.mips_store_preserved_registers()
        # Now we know the frame size so we can make room on the stack
        # (subiu = subtract immediate unsigned = supported by Mars MIPS)
        increase_stack_with = frame_size + self.mips_stack_pointer
        ret += f'{self.code_indent_string()}subiu $sp, $sp, {increase_stack_with}\n'
        ret += self._param_list_node.mips_store_arguments()
        ret += temp_ret
        # Give them some addresses aswell
        self._expression_node.mips_assign_address()

        # 4 Fill in the function body
        ret += f"{self.code_indent_string()}".join([child.generate_mips(c_comment) for child in self._children[1:]])
        # Some awesome code here

        # 5 Make a Return label, free up the stack, set s register's back in place and jump back to caller
        ret += f'\n{self.code_indent_string()}{self.code_function_base_label}_return:'
        self.increase_code_indent()
        ret += self.mips_load_preserved_registers(load_preserved_regs_from)
        ret += f'{self.code_indent_string()}addiu $sp, $sp, {increase_stack_with}\n'
        ret += f"{self.code_indent_string()}jr $ra\n"
        self.decrease_code_indent()
        self.decrease_code_indent()
        return ret

    def mips_register_available(self) -> bool:
        """
        Return's True if their is a register available, False if not (Variables should be stored on stack then)
        :return bool:  A bool = True if register(s) are available Else = False
        """
        return True if (self._preserve_mips_registers_available or self._lazy_mips_registers_available) else False

    def mips_get_available_register(self) -> str:
        """
        Return's a available register. Start's with the register the function doesn't need to preserve
        :return string: A register string
        """
        return self._preserve_mips_registers_available.pop() if self._preserve_mips_registers_available else \
            self._lazy_mips_registers_available.pop()

    def mips_store_preserved_registers(self) -> str:
        """
        Returns a string of store operations for the preservation registers
        :return string: mips string with store to RAM operations.
        """
        # Get the list of register's we need to save on the stack
        store = list(set(self.__class__._PRESERVE_MIPS_REGISTERS) - set(self._preserve_mips_registers_available))
        store.sort()
        ret = self.code_indent_string() + f'\n{self.code_indent_string()}' \
            .join([f'sw ${reg},'f' {index * MIPS_REGISTER_SIZE + self.mips_stack_pointer}($sp)'
                   for index, reg in enumerate(store)])

        ret += '\n'
        self.mips_increase_stack_pointer(MIPS_REGISTER_SIZE * len(store))
        return ret

    def mips_load_preserved_registers(self, load_from) -> str:
        """
        Returns a string of load operation's to load the s register's back into their register place
        :return:
        """

        load = list(set(self.__class__._PRESERVE_MIPS_REGISTERS) - set(self._preserve_mips_registers_available))
        load.sort()
        ret = self.code_indent_string() + f'\n{self.code_indent_string()}' \
            .join([f'lw ${reg}, {index * MIPS_REGISTER_SIZE + load_from}($sp)'
                   for index, reg in enumerate(load)])

        ret += "\n"
        return ret

    @property
    def code_function_base_label(self) -> str:
        return self.id

    @property
    def mips_stack_pointer(self) -> int:
        """
        :return int: The relative address of the stack pointer. Front end book keeping
        """
        return self._mips_stack_pointer

    def mips_increase_stack_pointer(self, amount: int) -> int:
        """
        Increases the amount of the stack pointer.
        :param int amount: the amount we increase the stack pointer with
        :return int: the new (relative value of the stack pointer)
        """
        self._mips_stack_pointer += amount
        return self._mips_stack_pointer

    # Meta Code Generation
    # ==================================================================================================================
    def comment_code(self, c_comment: bool = True, mips=True):
        """
        Generates the comment code
        :param mips:
        :param c_comment:
        :return: a string with comment code
        """
        # Code for a function Def in LLVM: Example: LLVM: Define i32 @main(int) {...} <=> C: int main(int){...}
        # Commenting...
        function_signature = self._param_list_node.generate_llvm_function_signature()
        return_type = f'{"".join([str(child) for child in self._type_stack[:-1]])} '

        return self.mips_comment(f'{return_type} {self.id}({function_signature}){{...}}', c_comment) if mips else \
            self.llvm_comment(f'{return_type} {self.id}({function_signature}){{...}}', c_comment)
