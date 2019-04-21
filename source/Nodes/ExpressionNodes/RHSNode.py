"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import Operator, TypeSpecifier


class RHSNode(ExpressionNode):
    _operator: Operator
    _parent_node: ExpressionNode

    def __init__(self, parent_node: ExpressionNode, **kwargs):
        super().__init__(parent_node)

        self._operator = kwargs.get('operator', Operator.DEFAULT)
        self._neg = kwargs.get("negative", False)

    def generate_llvm(self):
        ret = ""
        if len(self._children) == 1:  # Unary expression
            return self._children[0].generate_llvm()

        if len(self._children) == 2:  # Binary expression
            ret += self._children[0].generate_llvm()
            index1 = self.register_index

            ret += self._children[1].generate_llvm()
            index2 = self.register_index

            flt = ""
            if self.base_type == TypeSpecifier.FLOAT:
                flt += "f"

            if self._operator == Operator.DIV and self.base_type == TypeSpecifier.FLOAT:
                operating_word = "fdiv"
            else:
                operating_word = self._operator.bin_operator_map()
            self.increment_register_index()
            ret += "%{0} = {1} {2} %{3}, %{4}\n".format(self.register_index, operating_word,
                                                      self.base_type.llvm_type, index1, index2)
        return ret

    @property
    def label(self):
        if self._neg:
            return '"* -1"'

        return '"{0}"'.format(self._operator.value)

    @property
    def base_type(self):
        return self._parent_node.base_type
