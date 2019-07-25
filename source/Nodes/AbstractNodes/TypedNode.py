import abc

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import type_specifier
from Nodes.AbstractNodes import TypeModifierNode


class TypedNode(AbstractNode.AbstractNode, abc.ABC):
    """
    Superclass for all classes who have knowledge about their type. (Declarations right side id's expressions...)
    """

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._type_modifier_node = None  # Start of the type modifier subtree this can be *, [], ()
        self._type_stack = []

    # AST-generation
    # ==================================================================================================================

    def add_child(self, child: "AbstractNode", index: int = None):

        if isinstance(child, TypeModifierNode.TypeModifierNode):
            self._type_modifier_node = child

        super().add_child(child, index)

    def remove_child(self, child):
        if isinstance(child, TypeModifierNode.TypeModifierNode):
            self._type_modifier_node = None

        super().remove_child(child)

    @property
    def type_modifier_node(self):
        return self._type_modifier_node

    @type_modifier_node.setter
    def type_modifier_node(self, value):
        self._type_modifier_node = value

    # Semantic-analysis
    # ==================================================================================================================
    @property
    def type_stack(self):
        """ No outer modification on the list"""
        return list(self._type_stack)

    def type_stack_ref(self):
        """
        So we can modify the type stack from outer nodes
        :return:
        """
        return self._type_stack

    def set_base_type(self, tp):

        if isinstance(tp, str):
            tp = type_specifier.TypeSpecifier(tp)

        self._type_stack.append(tp)

    def _generate_type_modifier_stack(self, messenger) -> bool:
        """
        Generates the type modifier stack. This is a stack of type modifier types that will determine the modifiers
        applied on the node. See the TypeModifier enum for choices.
        :return: Bool
        """
        if self._type_modifier_node:
            return self._type_modifier_node.generate_type_operator_stack(self, messenger)

        return True

    def remove_modifier_node(self):

        if self._type_modifier_node:
            if self._type_modifier_node._type_modifier_node:
                return self._type_modifier_node.remove_bottom_node()
            else:
                self.remove_child(self._type_modifier_node)
