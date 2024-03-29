"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import TYPE_CHECKING
import Nodes.AbstractNodes.AbstractNode as AbstractNode
from Nodes.FunctionNodes.ReturnNode import ReturnNode

if TYPE_CHECKING:
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

    def has_return_node(self):

        for child in self.get_children():
            if isinstance(child, ReturnNode):
                return True

        return False

    # Mips-Code
    # ==================================================================================================================
    def mips_get_stack_pointer(self):
        return self._parent_node.mips_stack_pointer

    def mips_assign_register(self):
        [child.mips_assign_register() for child in self._children]

    def mips_assign_address(self):
        [child.mips_assign_address() for child in self._children]
