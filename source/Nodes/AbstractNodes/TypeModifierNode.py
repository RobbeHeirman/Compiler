"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes import AbstractNode

import typing

import Nodes.AbstractNodes.AbstractNode as AbstractNode

import type_specifier

from typing import TYPE_CHECKING

from type_specifier import TypeSpecifier

if TYPE_CHECKING:
    import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class TypeModifierNode(AbstractNode.AbstractNode):
    # TypeAnnotations
    _parent_node: typing.Union[
        "TypeModifierNode", "DeclarationNode.DeclarationNode", "ExpressionNode.ExpressionNode"]
    _type_modifier_node: "TypeModifierNode"
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

    def __repr__(self):
        try:
            return self._modifier_type.value

        except AttributeError:
            return "huh"

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

        try:
            super().remove_child(child)
            if isinstance(child, TypeModifierNode):
                self._type_modifier_node = None
        except:
            print("should be called")
            pass

    def add_child(self, child, index=None):

        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = child

        else:
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
        if self.modifier_type == type_specifier.TypeSpecifier.FUNCTION:
            self.modifier_type.function_signature = self._param_list_node.get_function_signature()
        node.type_stack_ref().append(self._modifier_type)
        if self._type_modifier_node is not None:
            self._type_modifier_node.generate_type_operator_stack(node, messenger)

        return True

    # LLVM Code generations
    # ==================================================================================================================

    def is_function_call(self):
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        elif self.modifier_type == type_specifier.TypeSpecifier.FUNCTION:
            return True
        return False

    def taking_address(self):
        if self._type_modifier_node:
            return self._type_modifier_node.taking_address()
        elif self.modifier_type == type_specifier.TypeSpecifier.ADDRESS:
            return True
        return False

    def do_we_dereference(self):
        if self._type_modifier_node:
            return self._type_modifier_node.taking_address()
        elif self.modifier_type == type_specifier.TypeSpecifier.POINTER:
            return True
        return False

    def get_param_node(self):
        if self._type_modifier_node:
            return self._type_modifier_node.get_param_node()
        return self._param_list_node

    def remove_bottom_node(self):

        if self._type_modifier_node:
            if self._type_modifier_node._type_modifier_node:
                return self._type_modifier_node.remove_bottom_node()

            else:
                self.remove_child(self._type_modifier_node)
