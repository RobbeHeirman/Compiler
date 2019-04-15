"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.LeafNode import LeafNode
from source.Specifiers import TypeSpecifier
from source.SymbolTable import Attributes


class DeclaratorNode(LeafNode):

    @property
    def label(self) -> str:
        return self._value

    # TODO: Declarator's are just id's for the time being.
    def __init__(self, parent_node, filename, ctx):
        """
        Initializer
        :param parent_node:
        :param filename:
        :param ctx:
        """
        super().__init__(parent_node, filename, ctx)

        attribute = Attributes(TypeSpecifier.DEFAULT, filename, self._line, self._column)
        self._parent_node.add_to_scope_symbol_table(self.value, attribute)

