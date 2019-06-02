"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import copy

import LlvmCode
import messages
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode
from Specifiers import DeclaratorSpecifier, TypeSpecifier
from SymbolTable import Attributes


class IdentifierExpressionNode(ExpressionNode):
    id: str

    def __init__(self, parent_node, identifier: str):
        super().__init__(parent_node)
        self.id = identifier
        self.base_type = TypeSpecifier.DEFAULT
        self.type_stack = []

    @property
    def label(self) -> str:
        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    def semantic_analysis(self):
        self.type_stack = self.find_type_stack()
        attrib = Attributes(self.base_type, self.type_stack, self.filename, self.line, self.column)
        ret = True
        if self.is_in_table(self.id):
            attr = self.get_attribute(self.id)
            self.base_type = attr.decl_type
            # Now we need to check if the operations done on the identifier are legal
            if not len(self.type_stack) is 0:
                attr_stack = copy.copy(attr.operator_stack)
                type_stack_cp = copy.copy(self.type_stack)
                if not self._stack_analysis(type_stack_cp, attr_stack):
                    ret = False

                # if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.FUNC:  # Now check the signature
                #   if attr.rhs_same_signature(self._parent_node.get_function_signature(), attrib, attr,
                #                             self.identifier):
                #       pass
                #   else:
                #    ret = False

        else:
            messages.error_undeclared_var(self.id, attrib)

        return ret

    def generate_llvm(self):
        ret = self.indent_string() + ";... {0}\n".format(self.id)
        ret += LlvmCode.llvm_load_instruction(self.base_type, self.id, self.type_stack, self.base_type,
                                              str(self.register_index), self.type_stack, self.indent_string())

        take_address = False
        if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.ADDRESS:
            take_address = True
            self.type_stack = self.type_stack[:-1]

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

        return ret
