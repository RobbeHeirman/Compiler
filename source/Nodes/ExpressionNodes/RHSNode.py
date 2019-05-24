"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum, auto

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Nodes.ExpressionNodes.ConstantNode import ConstantNode
from Nodes.ExpressionNodes.FixNode import FixNode, FixType
from Nodes.ExpressionNodes.IdNode import IdNode
from Specifiers import Operator, TypeSpecifier


class RHSNodeType(Enum):
    BINARY_OPERATOR = auto()
    CONSTANT = "Constant: "
    IDENTIFIER = "Identifier: "
    PTR = "*"
    ADDR = "&"
    ARRAY = "[]"
    FUNCTION = "()"


class RHSNode(ExpressionNode):
    type: RHSNodeType
    operator: Operator
    _parent_node: ExpressionNode

    def __init__(self, parent_node: ExpressionNode, **kwargs):

        super().__init__(parent_node)

        self.operator = kwargs.get('operator', Operator.DEFAULT)
        self.neg = kwargs.get("negative", False)
        self.type = None
        self.identifier = None
        self.constant = None

        self._member_operator_node = None
        self._identifier_node = None
        self._constant_node = None
        self._extra_node = None  # for array expression and function signatures

    @property
    def label(self):
        ret = "RHS"
        if self.neg:
            ret += '* -1'
        if self.operator is not Operator.DEFAULT:
            ret += "\n{0}".format(self.operator.value)

        else:
            if self.type is not None:
                ret += "\n{0}".format(self.type.value)

                if self.type is RHSNodeType.IDENTIFIER:
                    ret += "{0}".format(self.identifier)
                elif self.type is RHSNodeType.CONSTANT:
                    ret += "{0}".format(self.constant)
        return ret

    def add_child(self, child):

        if isinstance(child, IdNode):
            self._identifier_node = child
            self.type = RHSNodeType.IDENTIFIER

        elif isinstance(child, ConstantNode):
            self._constant_node = child
            self.type = RHSNodeType.CONSTANT

        elif isinstance(child, FixNode):
            self._member_operator_node = child

        super().add_child(child)

    def first_pass(self):

        if self._member_operator_node is not None:
            if self._member_operator_node.f_type == FixType.PTR:
                self.type = RHSNodeType.PTR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ADDRESS:
                self.type = RHSNodeType.ADDR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ARRAY:
                self.type = RHSNodeType.ARRAY

                self._member_operator_node.rhs_node.parent = self
                self.add_child(self._member_operator_node.rhs_node)
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

        elif self._identifier_node is not None:
            self.type = RHSNodeType.IDENTIFIER
            self.identifier = self._identifier_node.value
            self.remove_child(self._identifier_node)
            self._identifier_node = None

        elif self._constant_node is not None:
            self.type = RHSNodeType.CONSTANT
            self.constant = self._constant_node.value
            self.remove_child(self._constant_node)
            self._constant_node = None

        for child in self._children:
            child.first_pass()

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
