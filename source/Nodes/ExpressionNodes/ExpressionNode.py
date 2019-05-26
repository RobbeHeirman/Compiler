from abc import ABC
from enum import Enum, auto

from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Nodes.ExpressionNodes.FixNode import FixType, FixNode
from Nodes.ExpressionNodes.IdNode import IdNode


class ExpressionNodeType(Enum):
    BINARY_OPERATOR = auto()
    CONSTANT = "Constant: "
    IDENTIFIER = "Identifier: "
    PTR = "*"
    ADDR = "&"
    ARRAY = "[]"
    FUNCTION = "()"


class ExpressionNode(NonLeafNode, ABC):
    _BASE_LABEL = "expression"

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._identifier_node = None
        self._member_operator_node = None
        self.type = None
        self.identifier = None

    @property
    def label(self):
        ret = self._BASE_LABEL
        if self.type is not None:
            ret += "\n{0}".format(self.type.value)

            if self.type is ExpressionNodeType.IDENTIFIER:
                ret += "{0}".format(self.identifier)
        return ret

    def add_child(self, child: AbstractNode):

        if isinstance(child, IdNode):

            self._identifier_node = child
            self.type = ExpressionNodeType.IDENTIFIER

        elif isinstance(child, FixNode):
            self._member_operator_node = child

        super().add_child(child)

    def _handle_member_operator_node(self):

        if self._member_operator_node is not None:
            if self._member_operator_node.f_type == FixType.PTR:
                self.type = ExpressionNodeType.PTR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ADDRESS:
                self.type = ExpressionNodeType.ADDR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ARRAY:
                self.type = ExpressionNodeType.ARRAY

                self._member_operator_node.rhs_node.parent = self
                self.add_child(self._member_operator_node.rhs_node)
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.FUNCTION:
                self.type = ExpressionNodeType.FUNCTION
                self._member_operator_node.rhs_node.parent = self
                self.add_child(self._member_operator_node.rhs_node)
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

    def _handle_identifier_node(self):
        if self._identifier_node is not None:
            self.type = ExpressionNodeType.IDENTIFIER
            self.identifier = self._identifier_node.value
            self.remove_child(self._identifier_node)
            self._identifier_node = None

    def first_pass(self):

        self._handle_member_operator_node()
        self._handle_identifier_node()

        for child in self._children:
            child.first_pass()
