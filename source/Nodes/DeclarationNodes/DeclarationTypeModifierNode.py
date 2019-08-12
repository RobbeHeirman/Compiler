"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import typing
import type_specifier

from typing import TYPE_CHECKING

from Nodes.AbstractNodes import TypeModifierNode

from type_specifier import TypeSpecifier

if TYPE_CHECKING:
    import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class TypeModifierNode(TypeModifierNode.TypeModifierNode):
    """
    We use this node to handle prefix/postfix hierarchy.
    We can omit this in a future pass. This node has no actual info about the program.
    """

    # TypeAnnotations
    _parent_node: typing.Union["TypeModifierNode", "DeclarationNode.DeclarationNode", "ExpressionNode.ExpressionNode"]
    _type_modifier_node: "TypeModifierNode"
    _modifier_type: TypeSpecifier

    _BASE_LABEL = "TypeModifier"

    # Built-ins
    # ==================================================================================================================
    # AST-Generation
    # ==================================================================================================================

    # semantic analysis
    # ==================================================================================================================

    def generate_secondary_type(self, node: "DeclarationNode.DeclarationNode", messenger):
        """
        This function generates the operators stack.
        :param node:
        :param messenger:
        :return: the type_stack
        """
        if self.modifier_type == type_specifier.TypeSpecifier.FUNCTION:
            self.modifier_type.function_signature = self._param_list_node.get_function_signature()

        elif self.modifier_type == type_specifier.TypeSpecifier.ARRAY:
            self._param_list_node: ExpressionNode.ExpressionNode
            self._param_list_node.semantic_analysis(messenger)

            if self._param_list_node and self._param_list_node.type_stack[-1] != type_specifier.TypeSpecifier.INT:
                messenger.error_size_not_integer(node.id, self.line, self.column)

        node.type_stack_ref().append(self._modifier_type)

        if self._type_modifier_node is not None:
            self._type_modifier_node.generate_secondary_type(node, messenger)

        return True

    def get_static_size(self) -> int:
        if not self._type_modifier_node:
            if self.modifier_type == type_specifier.TypeSpecifier.ARRAY and self._param_list_node:
                return int(self._param_list_node.constant)

            else:
                return -1

        return self._type_modifier_node.get_static_size()



    # LLVM Code generations
    # ==================================================================================================================

