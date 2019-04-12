"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes import BaseTypeNode
from source.Nodes.AbstractNode import AbstractNode


class DeclarationNode(AbstractNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _base_type_node: BaseTypeNode
    label = "Declaration"

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._base_type_node = None

    def add_child(self, child: AbstractNode):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param child: An abstractNode
        """

        if isinstance(BaseTypeNode, type(child)):
            self._base_type_node = child

        super().add_child(child)


