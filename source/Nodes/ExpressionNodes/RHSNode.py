"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Nodes.ExpressionNodes.ConstantNode import ConstantNode
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode, ExpressionNodeType
from Specifiers import Operator, TypeSpecifier


class RHSNode(ExpressionNode):
    type: ExpressionNodeType
    operator: Operator
    _parent_node: NonLeafNode

    _BASE_LABEL = "RHS"

    def __init__(self, parent_node: NonLeafNode, **kwargs):

        super().__init__(parent_node)

        self.operator = kwargs.get('operator', Operator.DEFAULT)
        self.neg = kwargs.get("negative", False)
        self.constant = None

        self._constant_node = None
        self._extra_node = None  # for array expression and function signatures

    @property
    def label(self):
        ret = self._BASE_LABEL
        if self.neg:
            ret += '* -1'
        if self.operator is not Operator.DEFAULT:
            ret += "\n{0}".format(self.operator.value)

        else:
            if self.type is not None:
                ret += "\n{0}".format(self.type.value)

                if self.type is ExpressionNodeType.IDENTIFIER:
                    ret += "{0}".format(self.identifier)
                elif self.type is ExpressionNodeType.CONSTANT:
                    ret += "{0}".format(self.constant)
        return ret


    def add_child(self, child):

        if isinstance(child, ConstantNode):
            self._constant_node = child
            self.type = ExpressionNodeType.CONSTANT

        super().add_child(child)

    def first_pass(self):

        if self._constant_node is not None:
            self.type = ExpressionNodeType.CONSTANT
            self.constant = self._constant_node.value
            self.remove_child(self._constant_node)
            self._constant_node = None
        super().first_pass()

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

            if self.operator == Operator.DIV and self.base_type == TypeSpecifier.FLOAT:
                operating_word = "fdiv"
            else:
                operating_word = self.operator.bin_operator_map()
            self.increment_register_index()
            ret += "%{0} = {1} {2} %{3}, %{4}\n".format(self.register_index, operating_word,
                                                        self.base_type.llvm_type, index1, index2)
        return ret

    @property
    def base_type(self):
        return self._parent_node.base_type
