"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from source.Nodes.ExpressionNode import ExpressionNode
from source.Nodes.LeafNode import LeafNode
from source.Specifiers import TypeSpecifier


class BaseTypeNode(LeafNode):

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
