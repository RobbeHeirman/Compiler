"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC

from antlr4 import ParserRuleContext

from source.Nodes.AbstractNode import AbstractNode


class LeafNode(AbstractNode, ABC):
    """
    Represents all leaf nodes
    """
    _value: str
    _column: int
    _line: int
    _filename: str

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        """

        :param parent_node:
        :param filename:
        :param ctx: ParserRuleContextNode
        """
        super().__init__(parent_node)
        start = ctx.start
        self._filename = filename
        self._line = start.line
        self._column = start.column
        self._value = ctx.getText()

    @property
    def value(self):
        return self._value

    @property
    def filename(self):
        return self._filename

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    def generate_llvm(self):
        return ""
