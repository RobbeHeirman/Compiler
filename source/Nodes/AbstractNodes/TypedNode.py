import abc
from typing import List

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.DeclarationNodes.TypeModifierNode as TypeModifierNode
from Specifiers import TypeSpecifier, TypeModifier


class TypedNode(AbstractNode.AbstractNode, abc.ABC):
    """
    Superclass for all classes who have knowledge about their type. (Declarations right side id's expressions...)
    """

    _type_modifier_node: TypeModifierNode
    base_type: TypeSpecifier
    _type_stack: List[TypeModifier]

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._type_modifier_node = None  # Start of the type modifier subtree this can be *, [], ()

        self.base_type = None
        self._type_stack = []

    def _generate_type_modifier_stack(self):
        """
        Generates the type modifier stack. This is a stack of type modifier types that will determine the modifiers
        applied on the node. See the TypeModifier enum for choices.
        :return: None
        """
        if self._type_modifier_node:
            self._type_stack = self._type_modifier_node.generate_type_operator_stack()
