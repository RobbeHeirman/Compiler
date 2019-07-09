"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

# import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Specifiers


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    id: str

    def __init__(self, parent_node, ctx, filename):
        super().__init__(parent_node)
        self.id = ctx.getText()
        self.line = ctx.start.line
        self.column = ctx.start.column
        self.filename = filename
        self.base_type = Specifiers.TypeSpecifier.DEFAULT

        self._l_value = True  # As it's base form an identifier is an Lvalue

    @property
    def label(self) -> str:
        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    def semantic_analysis(self):

        self._generate_type_modifier_stack()  # the modifiers applied in the expression
        ret = True
        if self.is_in_table(self.id):
            attr = self.get_attribute(self.id)
            self.base_type = attr.decl_type  # this is the base type
            # Now we need to check if the operations done on the identifier are legal
            if not len(self._type_stack) is 0:
                if not self._stack_analysis(attr.operator_stack):
                    ret = False

                # if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.FUNC:  # Now check the signature
                #   if attr.rhs_same_signature(self._parent_node.get_function_signature(), attrib, attr,
                #                             self.identifier):
                #       pass
                #   else:
                #    ret = False

        else:
            self.__class__._messages.error_undeclared_var(self.id, self.filename, self.line, self.column)

        return ret

    def _stack_analysis(self, attr_stack) -> bool:
        """"
        Checks the type modifier corresponding to the expression vs the modifier's corresponding to the attributes.
        Modifies the expression's modifier stack to correspond the correct type.
        :param attr_stack. The stack found in the symbol table corresponding to the identifier
        :return: True if successful without semantic errors
        """

        # This is the attributes we retrieved from the symbol table. Note that the operators stored
        # in the symbol correspond to other operation on the right side of an assignment.
        # * means dereference while on lhs this declares that the variable will contain an address.
        # For comparison purposes we will make the meaning on rhs uniform so * lhs becomes & (address of) rhs.

        nw_stack = list(attr_stack)
        for element in reversed(self._type_stack):
            # if it's a * we dereference the value, meaning that we need to derefe a ptr type.
            if element == Specifiers.TypeModifier.PTR:
                if nw_stack[-1] == Specifiers.TypeModifier.PTR:  # Impicit convertion to R value in an id node
                    nw_stack.pop()
                    self._l_value = True

            if element == Specifiers.TypeModifier.ADDRESS:
                if not self._l_value:  # We need an L value to take an address from
                    self.__class__._messages.error_lvalue_required_addr_operand(self.filename, self.line, self.column)
                    return False

                else:
                    nw_stack.append(Specifiers.TypeModifier.PTR)  # Denoting this is address of R value
                    self._l_value = False

        self._type_stack = nw_stack
        return True

    def generate_llvm(self):
        # self.increment_register_index()
        # ret = self.indent_string() + ";... {0}\n".format(self.id)
        # ret += LlvmCode.llvm_load_instruction(self.base_type, self.id, self.type_stack, self.base_type,
        #                                       str(self.register_index), self.type_stack, self.indent_string())
        #
        # take_address = False
        # if self.type_stack and self.type_stack[-1] is TypeModifier.ADDRESS:
        #     take_address = True
        #     self.type_stack = self.type_stack[:-1]
        #
        # if self.type_stack and self.type_stack[-1] is TypeModifier.PTR:
        #     self.type_stack = self.type_stack[:-1]
        #     loading_from = self.register_index
        #     self.increment_register_index()
        #     # ret += LlvmCode.llvm_load_instruction(self.base_type, str(loading_from), self.type_stack,
        #     #                                       self.base_type,
        #     #                                       str(self.register_index), self.type_stack,
        #     #                                       self.indent_string())
        #
        # if take_address:
        #     prev_index = self.register_index
        #     self.increment_register_index()
        #     # ret += LlvmCode.llvm_allocate_instruction(str(self.register_index), self.base_type, self.type_stack,
        #     #                                           self.indent_string())
        #     #
        #     # ret += LlvmCode.llvm_store_instruction(self.base_type, str(prev_index), self.type_stack,
        #     #                                        self.base_type, str(self.register_index), self.type_stack,
        #     #                                        self.indent_string())
        #
        # return ret
        pass
