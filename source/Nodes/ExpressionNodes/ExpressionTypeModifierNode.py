"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import Nodes.AbstractNodes.TypeModifierNode as TypeModifierNode
import messages
import type_specifier
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class ExpressionTypeModifierNode(TypeModifierNode.TypeModifierNode):
    """
    Handles TypeModifiers like & () * .... In an expressionNode.
    Augment's the type of an expression.
    """
    _type_modifier_node: "ExpressionTypeModifierNode"

    # Built-in
    # ==================================================================================================================
    def __init__(self, parent_node, ctx, modifier=None):
        super().__init__(parent_node, ctx, modifier)

        self._llvm_used = False

    # Semantic analysis
    # ==================================================================================================================
    def generate_secondary_type(self, node: ExpressionNode.ExpressionNode, messenger: messages.MessageGenerator):
        """
        Function requires an expressionNode and adjust this node's type trough it's type stack.
        This node modifies the ExpressionNode state in type_stack and l_value(bool that tell's if l or r val)

        :param ExpressionNode node: ExpressionNode that we are modifying.
        :param MessageGenerator messenger: A messageGenerator that we use to generate error messages
        :return: bool: True if the modification's are legal, False if they are not.
        """
        if not self._type_modifier_node:
            if len(self._children) < 1:
                self._param_list_node = None
        else:
            if len(self._children) < 2:
                self._param_list_node = None

        # Check the type_modifier subtree. Children of this type modifier node get to modify the type stack first.
        if self._type_modifier_node:
            if not self._type_modifier_node.generate_secondary_type(node, messenger):
                return False

        # else this node should be applied first == base

        # Meaning the Dereference operator
        if self._modifier_type == type_specifier.TypeSpecifier.POINTER:
            # We can only dereference pointer types.
            if node.type_stack_ref()[-1].value == type_specifier.TypeSpecifier.POINTER:
                # If we dereference the type loses it's 'ptr' type
                node.type_stack_ref().pop()
                # Dereference operator returns a lvalue
                node.l_value = True

            else:
                messenger.error_unary_not_ptr(self._line, self._column)
                return False

        # Ref operator value becomes an address
        elif self._modifier_type == type_specifier.TypeSpecifier.ADDRESS:
            if node.l_value:
                # At the right side POINTER means address of. Used for type matching but maybe i should create
                # an alias to make this line more clear.
                node.type_stack_ref().append(type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER))
                node.l_value = False

            else:
                messenger.error_lvalue_required_addr(node.line, node.column)
                return False

        # Function call,
        elif self._modifier_type == type_specifier.TypeSpecifier.FUNCTION:
            # We require a function. In C you can call pointers to functions so this must be extended.
            if node.type_stack_ref()[-1] == type_specifier.TypeSpecifier.FUNCTION:
                # The parameter's calls their expression's need to be checked for correctness.
                self._param_list_node.semantic_analysis(messenger)
                # for simplicity we == is overloaded. We can go in more detail about the function signatures as
                # extension

                if self.get_function_signature() == node.type_stack_ref()[-1].function_signature:
                    node.type_stack_ref().pop()

                else:
                    if not self._check_any_consistent(node.type_stack_ref()[-1].function_signature):
                        messenger.error_signature_does_not_match(self._line, self._column)
                        return False

            else:
                messenger.error_object_not_function(self._line, self._column)
                return False

        # Array's
        elif self._modifier_type == type_specifier.TypeSpecifier.ARRAY:
            # First check if we can subscript.
            if not node.type_stack_ref()[-1] == type_specifier.TypeSpecifier.ARRAY:
                messenger.error_subscript_not_array(self.line, self.column)
                return False

            if not self._param_list_node:
                messenger.error_expected_expression(self.line, self.column)
                return False

            if not self._param_list_node.type_stack[-1] == type_specifier.TypeSpecifier.INT:
                messenger.error_subscript_not_integer(self.line, self.column)
                return False
            node.type_stack_ref().pop()

        return True

    def _check_any_consistent(self, signature: List):
        func_sign = self.get_function_signature()
        signature = list(signature)

        if signature and signature[-1] == [type_specifier.TypeSpecifier.ANY]:

            signature.pop()
            for i in range(len(signature)):
                if signature[i] != func_sign[i]:
                    return False
            return True

        return False

    # LLVM Code
    # ==================================================================================================================
    def get_bottom_arr(self):

        if self._type_modifier_node:

            ret_val = self._type_modifier_node.get_bottom_arr()
            if ret_val != -1:
                return ret_val

        if self.modifier_type == type_specifier.TypeSpecifier.ARRAY and not self._llvm_used:
            self._llvm_used = True
            return self

        return -1
