"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Union

import LlvmCode
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class ParamListNode(AbstractNode.AbstractNode):
    # Type annotations
    _children: Union[List['DeclarationNode.DeclarationNode'], List['ExpressionNode.ExpressionNode']]

    label = "Param list"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

    # Semantic analysis
    # ==================================================================================================================
    def get_function_signature(self):
        self._children: List[DeclarationNode]
        return [child.type_stack for child in self._children]

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm_function_signature(self):
        ret = ""
        for child in self._children:
            ret += "{0}".format(child.type_stack[0].llvm_type)
            for d_type in child.type_stack[1:]:
                ret += d_type.value
            # ret += " %{0}".format(child.id)

            ret += ", "
        ret = ret[:-2]
        return ret

    def llvm_load_params(self) -> str:
        """
        Will load all parameters that are variables to temporal registers
        :return:
        """

        ret = ""
        for child in self._children:
            if isinstance(child, ExpressionNode.ExpressionNode):

                ret += child.llvm_load()

            elif isinstance(child, DeclarationNode.DeclarationNode):
                ret += child.generate_llvm()
        return ret

    def llvm_store_params(self):

        ret = ""
        for index, child in enumerate(self._children):
            attr = self.get_attribute(child.id)
            ret += LlvmCode.llvm_store_instruction(str(index), child.type_stack, attr.llvm_name, child.type_stack,
                                                        self.code_indent_string())

        return ret

    def llvm_call_param_nodes(self) -> str:
        return "".join([child.generate_llvm() for child in self._children])

    # Mips-Code
    # ==================================================================================================================

    def mips_assign_params_to_mem(self, top_of_stack: int):
        """
        Will assign the parameters to their memory addresses for mips. The first 4 get a register
        The other's will be found on the stack. (Following mips convention's)
        :param int top_of_stack: The top of the stack. 5th+ argument's are stored there. This is shared by caller and
                                 # callee
        :return int: The size on the frame needed by argument's. if every argument needs 4 bytes this would
                     be a number between 0 and 16.
        """

        # We will tell the symbol table where all variables can be found.
        # $a0 - $a3 are Registers where the first 4 argument's are passed in.
        # Bottom of the stack is also reserved for the argument's.
        needed_frame_size: int = 0
        registers_params: List[DeclarationNode.DeclarationNode] = self._children[:4]
        for index, child in enumerate(registers_params):
            attr = self._parent_node.get_attribute(child.id)  # Semantic analysis ensured this is in the table
            attr.mips_register = f'a{index}'  # $a0 - $a3
            # Front-end need's to know in case of storage on stack.
            attr.mips_stack_address = self._parent_node.mips_stack_pointer
            self._parent_node.mips_increase_stack_pointer(child.type_stack[-1].mips_stack_size)
            needed_frame_size += child.type_stack[-1].mips_stack_size

        # Rest of the argument's are on the stack
        stack_params: List[DeclarationNode.DeclarationNode] = self._children[4:]
        # Those argument's are shared with the callee. So they are above the frame of this routine
        # so Top of the stack + offset
        stack_offset = 0
        for element in reversed(stack_params):
            size_type = element.type_stack[-1]
            attr = self._parent_node.get_attribute(element.id)
            attr.mips_is_register = False
            attr.mips_stack_address = top_of_stack + stack_offset
            stack_offset = size_type.mips_stack_size

        return needed_frame_size

    def mips_store_arguments(self) -> str:
        """
        Generates the Mips Code to store the first argument's on the stack
        :return:
        """

        ret = ""
        local_sp = 0
        for index, child in enumerate(self._children[:4]):
            ret += f'{self.code_indent_string()}sw $a{index}, {local_sp}($sp)\n'
            local_sp += child.type_stack[-1].mips_stack_size

        return ret

    def mips_load_arguments(self, reg) -> str:

        extra_size_needed = sum(child.type_stack[-1].mips_stack_size for child in self._children[4:])
        ret = ""
        if extra_size_needed:
            ret += f'{self.code_indent_string()}subiu, $sp, $sp, {extra_size_needed}\n'

        # First 4 into registers $a0 - $a3
        for index, child in enumerate(self._children[:4]):
            child: ExpressionNode.ExpressionNode
            ret += child.mips_store_in_register(f'a{index}')

        # Rest of the argument's on the stack
        tmp_stack_ptr = 0
        for index, child in enumerate(self._children[4:]):
            ret += child.mips_store_in_register(reg)
            ret += f'{self.code_indent_string()}sw ${reg}, {tmp_stack_ptr}($sp)\n'
            tmp_stack_ptr += child.type_stack[-1].mips_stack_size

        return ret

    def mips_free_stack_of_arguments(self):

        extra_size_needed = sum(child.type_stack[-1].mips_stack_size for child in self._children[4:])
        return f'{self.code_indent_string()}addiu, $sp, $sp, {extra_size_needed} # For arguments passed trough stack\n'
