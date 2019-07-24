import abc

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import type_specifier


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
        print(self._line)
        if self._type_modifier_node:
            print()
            return self._type_modifier_node.generate_type_operator_stack(self, messenger)

        return True
