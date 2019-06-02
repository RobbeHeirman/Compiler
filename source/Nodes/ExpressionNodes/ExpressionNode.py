
from abc import ABC
from enum import Enum, auto
from typing import List

import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.FixNode import FixType, FixNode
from Specifiers import DeclaratorSpecifier
from SymbolTable import Attributes


class ExpressionNodeType(Enum):
    BINARY_OPERATOR = auto()
    CONSTANT = "Constant: "
    IDENTIFIER = "Identifier: "
    PTR = "*"
    ADDR = "&"
    ARRAY = "[]"
    FUNCTION = "()"

    @property
    def decl_specifier(self):
        specifier_map = {
            self.PTR: DeclaratorSpecifier.PTR,
            self.ADDR: DeclaratorSpecifier.ADDRESS,
            self.ARRAY: DeclaratorSpecifier.ARRAY,
            self.FUNCTION: DeclaratorSpecifier.FUNC
        }
        return specifier_map[self]


class ExpressionNode(AbstractNode, ABC):
    _BASE_LABEL = "expression"
    _OPERATOR_TYPES = [ExpressionNodeType.ARRAY,
                       ExpressionNodeType.PTR, ExpressionNodeType.ADDR, ExpressionNodeType.FUNCTION]

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._identifier_node = None
        self._member_operator_node = None

        self.base_type = None
        self.type = None

        # Book keeping info
        self.filename = None
        self.line = None
        self.column = None

    @property
    def type_string_llvm(self):
        return self.base_type.llvm_type + "*" * len(self.type_stack)

    @property
    def label(self):
        ret = self._BASE_LABEL + "\n"
        if self.base_type:
            ret += "Base type: " + self.base_type.value + "\n"

        return ret

    def add_child(self, child: AbstractNode, index=None):

        if isinstance(child, FixNode):
            self._member_operator_node = child

        super().add_child(child)

    def get_error_info(self):
        """
        :return: A tuple filename, line, column
        """
        if self.filename is None:
            for child in self._children:
                val = child.get_error_info()
                if val is not None:
                    return val
        else:
            return self.filename, self.line, self.column


    def _handle_member_operator_node(self):

        if self._member_operator_node is not None:
            if self._member_operator_node.f_type == FixType.PTR:
                self.type = ExpressionNodeType.PTR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ADDRESS:
                self.type = ExpressionNodeType.ADDR
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.ARRAY:
                self.type = ExpressionNodeType.ARRAY

                self._member_operator_node.rhs_node.parent = self
                self.add_child(self._member_operator_node.rhs_node)
                self._member_operator_node.rhs_node.parent_node = self
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None

            elif self._member_operator_node.f_type == FixType.FUNCTION:
                self.type = ExpressionNodeType.FUNCTION
                self._member_operator_node.rhs_node.parent = self
                self.add_child(self._member_operator_node.rhs_node)
                self._member_operator_node.rhs_node.parent_node = self
                self.remove_child(self._member_operator_node)
                self._member_operator_node = None



    def first_pass(self):
        self._handle_member_operator_node()
        for child in self._children:
            child.first_pass()

    def semantic_analysis(self) -> bool:
        """
        Semantic analysis in expressive nodes is looking up if the signature of the identifier matches the
        one in the symbol table.
        Note: We do not support implicit conversions.
        :return: 
        """

        ret = True
        for child in self._children:
            if not child.semantic_analysis():
                ret = False

        return ret

    def find_type_stack(self, stack=None) -> List[DeclaratorSpecifier]:
        """
        The expression node has an operator type stack. We need to find this type stack to check if we can handle
        the expression
        :param stack:
        :return:
        """
        if stack is None:
            stack = []

        if self.type in self._OPERATOR_TYPES:
            stack.append(self.type.decl_specifier)

            if not isinstance(self._parent_node, ExpressionNode):
                return stack
            else:
                return self._parent_node.find_type_stack(stack)
        else:
            if isinstance(self._parent_node, ExpressionNode):
                return self._parent_node.find_type_stack(stack)
        return []

    def _stack_analysis(self, own_stack, attr_stack) -> bool:
        """"
        Recursively calling this until all own stack symbols are matched.
        :return: True if successful without semantic errors
        """

        own_stack.reverse()  # More clearer operation on the stack
        if len(own_stack) is 0:
            return True

        attr = Attributes(self.base_type, own_stack, self.filename, self.line, self.column)

        if own_stack[-1] is DeclaratorSpecifier.ADDRESS:  # Need to check if applied on Lvalue
            own_stack.pop(-1)

            if not own_stack or own_stack[-1] is DeclaratorSpecifier.PTR:
                pass

            else:
                messages.error_lvalue_required_addr(attr)
                return False

        if not own_stack:
            return True

        if own_stack[-1] is DeclaratorSpecifier.PTR:
            if len(attr_stack) > 0 and attr_stack[-1] is DeclaratorSpecifier.PTR:
                pass
            else:
                messages.error_unary_not_ptr(attr)
                return False

        elif own_stack[-1] is DeclaratorSpecifier.ARRAY:
            if len(attr_stack) > 0 and attr_stack[-1] is DeclaratorSpecifier.ARRAY:
                pass
            else:

                messages.error_subscript_not_array(attr)
                return False

        elif own_stack[-1] is DeclaratorSpecifier.FUNC:
            if attr_stack and attr_stack[-1] is DeclaratorSpecifier.FUNC:
                pass
            else:
                messages.error_object_not_function(self.identifier, attr)

        if len(own_stack) > 0:
            own_stack.pop(-1)
        if len(attr_stack) > 0:
            attr_stack.pop(-1)

        return self._stack_analysis(own_stack, attr_stack)
