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

    def __init__(self, parent_node, value: str):  # TODO: Declarator's are just id's for the time being.
        super().__init__(parent_node, value)
