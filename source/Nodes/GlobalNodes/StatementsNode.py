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
    def mips_get_stack_pointer(self):
        return self._parent_node.mips_stack_pointer
