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

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._identifier_node = None
        self._type_modifier_node = None

        self.type = None

        self._l_value = True

        # Book keeping info
        self.filename = None
        self.line = None
        self.column = None

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
        ret = True
        for child in self._children:
            if not child.semantic_analysis(messenger):
                ret = False

        return ret

    def is_constant(self):
        return False
