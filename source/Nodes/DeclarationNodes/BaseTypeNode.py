"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Nodes.AbstractNodes.LeafNode import LeafNode
from Specifiers import TypeSpecifier


class BaseTypeNode(LeafNode):
    """
    Represents a base type Node.
    This is always a leaf_node
    """
    _value: TypeSpecifier

    def __init__(self, parent_node: ExpressionNode, filename: str, ctx: ParserRuleContext):
        """
        Initializer
        :param parent_node: parent node.
        :param filename: name of file yield is found.
        :param ctx: ParserRuleContext
        """
        super().__init__(parent_node, filename, ctx)
        self._value = TypeSpecifier(self._value)

    @property
    def label(self) -> str:
        return str(self._value.value)

    @property
    def value(self)-> TypeSpecifier:
        return self._value

    def llvm_code_value(self):
        pass

    def llvm_type(self):
        pass
