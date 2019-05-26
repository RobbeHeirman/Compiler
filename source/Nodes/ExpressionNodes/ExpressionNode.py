from abc import ABC
from enum import Enum, auto

from Nodes.AbstractNodes.NonLeafNode import NonLeafNode


class ExpressionNodeType(Enum):
    BINARY_OPERATOR = auto()
    CONSTANT = "Constant: "
    IDENTIFIER = "Identifier: "
    PTR = "*"
    ADDR = "&"
    ARRAY = "[]"
    FUNCTION = "()"


class ExpressionNode(NonLeafNode, ABC):
    pass
