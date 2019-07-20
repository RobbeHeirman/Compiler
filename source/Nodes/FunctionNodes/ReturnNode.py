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

    def generate_llvm(self):

        ret_type = self._parent_node.get_return_type()
        if isinstance(self._children[0], ConstantExpressionNode.ConstantExpressionNode):
            return self.indent_string() + "ret {0} {1}\n".format(ret_type[0].llvm_type, self._children[0].llvm_constant)
        return_string = self._children[0].generate_llvm()

        prev_index = self.register_index
        self.increment_register_index()
        return_string += LlvmCode.llvm_load_instruction(str(prev_index), ret_type, str(self.register_index), ret_type,
                                                        self.indent_string())

        return_string += self.indent_string() + "ret {0} %{1}\n".format(ret_type[0].llvm_type, self.register_index)
        return return_string

    def has_return(self):
        if self._children:
            return True
        return False
