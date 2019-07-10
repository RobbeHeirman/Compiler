from enum import Enum, auto
import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.DeclarationNodes.TypeModifierNode as TypeModifierNode
import Specifiers


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
            self.PTR: Specifiers.TypeModifier.PTR,
            self.ADDR: Specifiers.TypeModifier.ADDRESS,
            self.ARRAY: Specifiers.TypeModifier.ARRAY,
            self.FUNCTION: Specifiers.TypeModifier.FUNC
        }
        return specifier_map[self]


class ExpressionNode(TypedNode.TypedNode):
    _BASE_LABEL = "expression"
    _OPERATOR_TYPES = [ExpressionNodeType.ARRAY,
                       ExpressionNodeType.PTR, ExpressionNodeType.ADDR, ExpressionNodeType.FUNCTION]

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node)

        self.column = ctx.start.column
        self.line = ctx.start.line
        self.filename = filename

        self._identifier_node = None
        self._type_modifier_node = None

        self.type = None

        self._l_value = True

    @property
    def type_string_llvm(self):
        return self.base_type.llvm_type + "*" * len(self._type_stack)

    @property
    def label(self):
        ret = self._BASE_LABEL + "\n"
        if self.base_type:
            ret += "Base type: " + self.base_type.value + "\n"

        return ret

    def is_address(self):

        if self._type_stack and self._type_stack[-1] is Specifiers.TypeModifier.ADDRESS:
            return True

        return False

    def add_child(self, child, index=None):

        if isinstance(child, TypeModifierNode.TypeModifierNode):
            temp = self._type_modifier_node
            self._type_modifier_node = child
            if temp is not None:
                self.remove_child(temp)
                self._type_modifier_node.add_child(temp)
                temp.parent_node = self._type_modifier_node

        super().add_child(child)

    def get_error_info(self):
        """
        :return: A tuple filename, line, column
        """
        if self.filename is None:
            for _ in self._children:
                # val = child.get_error_info()
                val = ""
                if val is not None:
                    return val
        else:
            return self.filename, self.line, self.column

    def _handle_member_operator_node(self):
        if self._type_modifier_node is not None:
            if self._type_modifier_node.f_type == Specifiers.TypeModifier.PTR:
                self.type = ExpressionNodeType.PTR
                self.remove_child(self._type_modifier_node)
                self._type_modifier_node = None

            elif self._type_modifier_node.f_type == Specifiers.TypeModifier.ADDRESS:
                self.type = ExpressionNodeType.ADDR
                self.remove_child(self._type_modifier_node)
                self._type_modifier_node = None

            elif self._type_modifier_node.f_type == Specifiers.TypeModifier.ARRAY:
                self.type = ExpressionNodeType.ARRAY

                self._type_modifier_node.rhs_node.parent = self
                self.add_child(self._type_modifier_node.rhs_node)
                self._type_modifier_node.rhs_node.parent_node = self
                self.remove_child(self._type_modifier_node)
                self._type_modifier_node = None

            elif self._type_modifier_node.f_type == Specifiers.TypeModifier.FUNCTION:
                self.type = ExpressionNodeType.FUNCTION
                self._type_modifier_node.rhs_node.parent = self
                self.add_child(self._type_modifier_node.rhs_node)
                self._type_modifier_node.rhs_node.parent_node = self
                self.remove_child(self._type_modifier_node)
                self._type_modifier_node = None

    # def first_pass(self):
    #     self._handle_member_operator_node()
    #     for child in self._children:
    #         child.first_pass()

    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis in expressive nodes is looking up if the signature of the identifier matches the
        one in the symbol table.
        Note: We do not support implicit conversions.
        :return:
        """
        self._generate_type_modifier_stack()  # the modifiers applied in the expression
        ret = True

        if not self._stack_analysis(messenger, []):
            return False

        for child in self._children:
            if not child.semantic_analysis(messenger):
                ret = False

        return ret

    def is_constant(self):
        return False

    def _stack_analysis(self, messenger, attr_stack=None) -> bool:
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
        if attr_stack is None:
            attr_stack = []
        nw_stack = list(attr_stack)
        for element in reversed(self._type_stack):
            # if it's a * we dereference the value, meaning that we need to dereference a ptr type.
            if element == Specifiers.TypeModifier.PTR:
                if nw_stack[-1] == Specifiers.TypeModifier.PTR:  # Implicit conversion to R value in an id node
                    nw_stack.pop()
                    self._l_value = True

            if element == Specifiers.TypeModifier.ADDRESS:
                if not self._l_value:  # We need an L value to take an address from
                    messenger.error_lvalue_required_addr_operand(self.filename, self.line, self.column)
                    return False

                else:
                    nw_stack.append(Specifiers.TypeModifier.PTR)  # Denoting this is address of R value
                    self._l_value = False

        self._type_stack = nw_stack
        return True
