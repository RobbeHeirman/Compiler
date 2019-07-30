"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.FunctionNodes.FuncDefNode as FuncDefNode


class StatementsNode(AbstractNode.AbstractNode):
    label = "Statements"

    _parent_node: "FuncDefNode.FuncDefNode"

    # Built-in
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

    # LLVM Code
    # ==================================================================================================================
    def get_return_type(self):
        return self._parent_node.get_return_type()

    # Mips-Code
    # ==================================================================================================================
    def mips_get_stack_pointer(self):
        return self._parent_node.mips_stack_pointer

    def mips_stack_space_needed(self):
        """
        Return's The total mips stack size needed
        :return: Stack space needed by all children
        """
        return sum(child.mips_stack_space_needed() for child in self._children)

    def mips_assign_register(self):
        [child.mips_assign_register() for child in self._children]

    def mips_assign_address(self):
        [child.mips_assign_address() for child in self._children]
