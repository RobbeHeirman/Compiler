"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import abc

from Nodes.AbstractNodes import AbstractNode
import typing
import type_specifier
from typing import TYPE_CHECKING
from type_specifier import TypeSpecifier, TypeStack

if TYPE_CHECKING:
    import Nodes.AbstractNodes.TypedNode as TypedNode
    import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class TypeModifierNode(AbstractNode.AbstractNode, abc.ABC):
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

        super().remove_child(child)
        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = None

        elif isinstance(child, ExpressionNode.ExpressionNode):
            self._param_list_node = None

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

    @abc.abstractmethod
    def generate_secondary_type(self, node: "TypedNode.TypedNode", messenger) -> bool:
        """
        This function applies the secondary type to a given node. After application the node will represent
        a new type according to what this type modifier (node) introduced. The change of type is found in the
        type stack attribute of the Given (TypedNode)
        :param node: The node the type modification needs to be applied to.
        :param messenger: An error messenger Object. For generating error codes.
        :return: the type_stack
        """

    def generate_type_modifier_stack(self, type_modifier_stack: TypeStack = None) -> TypeStack:
        """
        Will generate a List of TypeSpecifiers elements in stack order. Add's own type to the list and recursively
        calls it's child. Until a child is a leaf.
        :return:
        """

        var_type_stack = type_modifier_stack if type_modifier_stack else []
        var_type_stack.append(self.modifier_type)
        if self._type_modifier_node:
            return self._type_modifier_node.generate_type_modifier_stack(var_type_stack)
        return var_type_stack

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
