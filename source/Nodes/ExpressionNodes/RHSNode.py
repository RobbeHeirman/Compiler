"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import struct

import LlvmCode
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.ConstantNode import ConstantNode
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode, ExpressionNodeType
from Nodes.FunctionNodes.ParamListNode import ParamListNode
from Specifiers import Operator, TypeSpecifier, DeclaratorSpecifier


class RHSNode(ExpressionNode):
    type: ExpressionNodeType
    operator: Operator

    _BASE_LABEL = "RHS"

    def __init__(self, parent_node: AbstractNode, **kwargs):

        super().__init__(parent_node)

        self.operator = kwargs.get('operator', Operator.DEFAULT)
        self.neg = kwargs.get("negative", False)
        self.constant = None

        self._constant_node = None
        self._extra_node = None  # for array expression and function signatures

    @property
    def label(self):
        ret = self._BASE_LABEL
        if self.neg:
            ret += '* -1'
        if self.operator is not Operator.DEFAULT:
            ret += "\n{0}".format(self.operator.value)

        else:
            if self.type is not None:
                ret += "\n{0}".format(self.type.value)

                if self.type is ExpressionNodeType.IDENTIFIER:
                    ret += "{0}".format(self.identifier)
                elif self.type is ExpressionNodeType.CONSTANT:
                    if self.base_type:
                        ret += "{0}\n".format(self.base_type.value)
                    ret += "{0}".format(self.constant)
        return ret

    def add_child(self, child, index=None):

        if isinstance(child, ConstantNode):
            self._constant_node = child
            self.type = ExpressionNodeType.CONSTANT
            self.filename = child.filename
            self.line = child.line
            self.column = child.column

        if isinstance(child, ParamListNode):
            self._extra_node = child

        super().add_child(child)

    def first_pass(self):

        if self._constant_node is not None:
            self.type = ExpressionNodeType.CONSTANT
            self.constant = self._constant_node.value
            self.base_type = self._constant_node.type

            self.filename = self._constant_node.filename
            self.line = self._constant_node.line
            self.column = self._constant_node.column

            self.remove_child(self._constant_node)
            self._constant_node = None
        super().first_pass()

    def generate_llvm(self):
        ret = ""

        if self.type is ExpressionNodeType.CONSTANT or self.type is ExpressionNodeType.IDENTIFIER:
            self.increment_register_index()

            if self.type is ExpressionNodeType.IDENTIFIER:
                self.constant = self.identifier
            take_address = False
            if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.ADDRESS:
                take_address = True
                self.type_stack = self.type_stack[:-1]

            if self.type is ExpressionNodeType.IDENTIFIER:

                ret += LlvmCode.llvm_load_instruction(self.base_type, self.identifier, self.type_stack, self.base_type,
                                                      str(self.register_index), self.type_stack, self.indent_string())

                if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.PTR:
                    self.type_stack = self.type_stack[:-1]
                    loading_from = self.register_index
                    self.increment_register_index()
                    ret += LlvmCode.llvm_load_instruction(self.base_type, str(loading_from), self.type_stack,
                                                          self.base_type,
                                                          str(self.register_index), self.type_stack,
                                                          self.indent_string())

            if take_address:
                prev_index = self.register_index
                self.increment_register_index()
                ret += LlvmCode.llvm_allocate_instruction(str(self.register_index), self.base_type, self.type_stack,
                                                          self.indent_string())

                ret += LlvmCode.llvm_store_instruction(self.base_type, str(prev_index), self.type_stack,
                                                       self.base_type, str(self.register_index), self.type_stack,
                                                       self.indent_string())

        if len(self._children) == 1:  # Unary expression
            return self._children[0].generate_llvm()

        if len(self._children) == 2:  # Binary expression
            ret += self._children[0].generate_llvm()
            index1 = self.register_index

            ret += self._children[1].generate_llvm()
            index2 = self.register_index

            flt = ""
            if self.base_type == TypeSpecifier.FLOAT:
                flt += "f"

            if self.operator == Operator.DIV and self.base_type == TypeSpecifier.FLOAT:
                operating_word = "fdiv"
            else:
                operating_word = self.operator.bin_operator_map()
            self.increment_register_index()
            ret += "%{0} = {1} {2} %{3}, %{4}\n".format(self.register_index, operating_word,
                                                        self.base_type.llvm_type, index1, index2)
        ret += self.indent_string() + "; end expression\n"
        return ret

    """
    @property
    def base_type(self):
        return self._parent_node.base_type
    """

    def get_function_signature(self):
        return self._extra_node.get_signature_list()
