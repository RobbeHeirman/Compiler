"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Nodes.GlobalNodes.StatementsNode as StatementsNode
import Nodes.ExpressionNodes.ConstantExpressionNode as ConstantExpressionNode
import Nodes.ExpressionNodes.IdentifierExpressionNode as IdentifierExpressionNode


class ReturnNode(AbstractNode.AbstractNode):
    label = "return"

    # Type Annotations
    _parent_node: StatementsNode.StatementsNode
    _children: List[ExpressionNode.ExpressionNode]

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node: AbstractNode.AbstractNode, ctx):
        super().__init__(parent_node, ctx)

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger):

        child = self._children[0]
        if not child.semantic_analysis(messenger):
            return False

        self._parent_node: StatementsNode.StatementsNode
        child: ExpressionNode.ExpressionNode
        if not child.type_stack == self._parent_node.get_return_type():
            messenger.error_conflicting_return_type(self._line, self._column)
            return False
        return True

    def has_return(self):
        if self._children:
            return True
        return False

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        # Commenting
        return_string = self.llvm_comment(f'return {self._children[0]}', c_comment)

        ret_type = self._parent_node.get_return_type()
        ret_type_str = ret_type[0].llvm_type
        ret_type_str += "".join([c_type.value for c_type in ret_type[1:]])
        if isinstance(self._children[0], ConstantExpressionNode.ConstantExpressionNode):
            child: ConstantExpressionNode.ConstantExpressionNode = self._children[0]
            return_string += self.code_indent_string() + "ret {0} {1}\n".format(ret_type_str, child.llvm_value)

        elif isinstance(self._children[0], IdentifierExpressionNode.IdentifierExpressionNode):
            child: IdentifierExpressionNode.IdentifierExpressionNode = self._children[0]
            return_string += child.llvm_load()
            return_string += self.code_indent_string() + "ret {0} %{1}\n".format(ret_type_str, self.register_index)

        return return_string

    # Mips Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True) -> str:
        """
        Generates The return Code in Mips. Will need to load a value into the Load register. Either $v0 or $v1.
        We will always use $v0 for consistency.
        :param bool c_comment: Do Write comments
        :return str: The return string with MIPS code and optional comment strings
        """

        # Start with commenting
        return_string = '\n' + self.mips_comment(f'return {self._children[0]}', c_comment)

        # Load the value into $v0 and jump to the return label
        child = self._children[0]

        return_string += child.mips_store_in_register('v0')
        return_string += f'{self.code_indent_string()}j {self._parent_node.mips_function_base_label}_return\n'
        return return_string
