from abc import ABC

from Nodes.AbstractNodes.AbstractNode import AbstractNode


class TypedNode(AbstractNode, ABC):
    """
    Superclass for all classes who have knowledge about their type. (Declarations right side id's expressions...)
    """

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self.id = None
        self.base_type = None
        self.type_stack = []
