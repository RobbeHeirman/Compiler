"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import typing

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import type_specifier

from typing import TYPE_CHECKING

from type_specifier import TypeSpecifier

if TYPE_CHECKING:
    import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class TypeModifierNode(AbstractNode.AbstractNode):
    """
    We use this node to handle prefix/postfix hierarchy.
    We can omit this in a future pass. This node has no actual info about the program.
    """

    # TypeAnnotations
    _parent_node: typing.Union["TypeModifierNode", "DeclarationNode.DeclarationNode", "ExpressionNode.ExpressionNode"]
    _type_modifier_node: "TypeModifierNode"
    _param_list_node: ParamListNode
    _modifier_type: TypeSpecifier

    _BASE_LABEL = "TypeModifier"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx, mod_type: type_specifier.TypeSpecifier = None):
        """
        Initializer
        :param parent_node: the parent node
        """
        super().__init__(parent_node, ctx)

        self._type_modifier_node = None  # Child type_modifier_node. Used for nested type modifiers
        self._param_list_node = None  # if the type modifier is a function call ref keeps track of the call signature

        self._modifier_type = mod_type
        self._is_implicit_conversion = False

    def __eq__(self, o):

        if self._modifier_type == o.modifier_type:
            if self.get_function_signature() == o.get_function_signature():
                return True

        return False

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):

        ret = self._BASE_LABEL
        if self._modifier_type is not None:
            ret += "\nType: {0}\n".format(self._modifier_type.value)
        else:
            ret += "??"

        if self._is_implicit_conversion:
            ret += "(implicit conversion)"
        return ret

    # AST-Generation
    # ==================================================================================================================
    @property
    def modifier_type(self):
        return self._modifier_type

    @modifier_type.setter
    def modifier_type(self, val):
        if isinstance(val, str):
            val = type_specifier.TypeSpecifier(val)
        self._modifier_type = val

    def remove_child(self, child):

        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = None

        super().remove_child(child)

    def add_child(self, child, index=None):

        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = child

        elif isinstance(child, ParamListNode.ParamListNode):
            self._param_list_node = child

        super().add_child(child)

    def add_id(self, identifier: str):
        """
        Will propagate an added id to the declaration node
        :param identifier: The id to propagate
        :return: None
        """
        self._parent_node.add_id(identifier)

    # def _add_id_node(self, child):
    #     self._id_node = child

    # semantic analysis
    # ==================================================================================================================
    def get_function_signature(self):
        if self._param_list_node:
            return self._param_list_node.get_function_signature()

        return []

    def generate_type_operator_stack(self, node, messenger):
        """
        This function generates the operators stack.
        :param node:
        :param messenger:
        :return: the type_stack
        """
        if self._type_modifier_node is not None:
            self._type_modifier_node.generate_type_operator_stack(node, messenger)

        node.type_stack_ref().append(self._modifier_type)
        return True

    # LLVM Code generations
    # ==================================================================================================================

    def is_function_call(self):
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        elif self.modifier_type == type_specifier.TypeSpecifier.FUNCTION:
            return True
        return False

    def get_param_node(self):
        if self._type_modifier_node:
            return self._type_modifier_node.get_param_node()
        return self._param_list_node
