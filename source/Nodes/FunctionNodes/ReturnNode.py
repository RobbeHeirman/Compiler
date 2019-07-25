"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import LlvmCode
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Nodes.GlobalNodes.StatementsNode as StatementsNode
import Nodes.ExpressionNodes.ConstantExpressionNode as ConstantExpressionNode
import Nodes.ExpressionNodes.IdentifierExpressionNode as IdentifierExpressionNode


class ReturnNode(AbstractNode.AbstractNode):
    label = "return"

    _parent_node: StatementsNode.StatementsNode
    _children: List[ExpressionNode.ExpressionNode]

    def __init__(self, parent_node: AbstractNode.AbstractNode, ctx):
        super().__init__(parent_node, ctx)

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

    def has_return(self):
        if self._children:
            return True
        return False
