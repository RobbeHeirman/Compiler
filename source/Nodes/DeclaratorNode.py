"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.LeafNode import LeafNode


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
