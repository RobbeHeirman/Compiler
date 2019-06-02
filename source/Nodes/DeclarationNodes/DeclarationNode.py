"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import LlvmCode
import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.ArrayInitNode import ArrayInitNode
from Nodes.ExpressionNodes.RHSNode import RHSNode
from Nodes.DeclarationNodes.DeclaratorNode import DeclaratorNode
from Nodes.FunctionNodes.ParamListNode import ParamListNode
from Specifiers import TypeSpecifier, DeclaratorSpecifier
from SymbolTable import Attributes
from typing import Union


class DeclarationNode(AbstractNode):
    """
    Represents a Declaration in our abstract syntax tree.
    Will deduct the base type of the declaration in the first pass.
    Has 1 or 2 children a declarator (will become a stack of pre and postfix type specifiers after first pass)
    An optional initializer as 2d child.
    """
    _declarator_node: DeclaratorNode
    _rhs_node: Union[RHSNode, ArrayInitNode]
    _lexeme: str

    _BASE_LABEL = "Declaration"

    def __init__(self, parent_node: AbstractNode):
        super().__init__(parent_node)

        # The 2 child nodes
        self._declarator_node = None
        self._rhs_node = None

        # Base info
        self._id = None  # Id can be deducted from children.
        self._base_type = None  # Base type gets passed from a decl_list node.

        self.type_stack = []

        # Error message info
        self._filename = None
        self._line = None
        self._column = None

    @property
    def label(self):
        ret_label = self._BASE_LABEL
        if self._base_type is not None:
            ret_label += "\\nBase type: {0}".format(self._base_type.value)

        if self._id is not None:
            ret_label += "\\n Identifier: {0}".format(self._id)

        return ret_label

    @property
    def id(self):
        return self._id

    @property
    def base_type(self):
        return self._base_type

    @property
    def type_string_llvm(self):
        return self.base_type.llvm_type + "*" * len(self.type_stack)

    def to_attribute(self):
        op_stack = []
        if self._declarator_node:
            op_stack = self._declarator_node.generate_type_operator_stack()
        return Attributes(self.base_type, op_stack,
                          self._filename, self._line, self._column)

    @base_type.setter
    def base_type(self, value: TypeSpecifier):
        self._base_type = value

    def dot_string(self) -> str:
        """Generates the visual representation of the node in .dot"""
        ret = AbstractNode.dot_string(self)

        if self._declarator_node is not None:
            ret += "{0}--{{".format(self._index)
            ret += "{0} ".format(self._declarator_node.index)
            ret += "}[label = \" Decl\" ]\n"

        if self._rhs_node is not None:
            ret += "{0}--{{".format(self._index)
            ret += "{0} ".format(self._rhs_node.index)
            ret += "}[label = \" = \" ]\n"

        for child in self._children:
            ret += child.dot_string()

        return ret

    def _add_declarator(self, child: DeclaratorNode):
        self._declarator_node = child

    def _add_rhs(self, child):
        self._rhs_node = child

    # Can we do something to make overloading more generic

    def add_child(self, child: Union[DeclaratorNode, RHSNode], index: int = None):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param index: index where to add
        :param child: An abstractNode
        """

        if isinstance(child, DeclaratorNode):
            self._add_declarator(child)

        elif isinstance(child, RHSNode) or isinstance(child, ArrayInitNode):
            self._add_rhs(child)

        else:
            print(type(child))
            print("something went wrong")
        super().add_child(child)

    def remove_child(self, child):

        if isinstance(child, DeclaratorNode):
            self._declarator_node = None

        super().remove_child(child)

    def first_pass(self):
        """
        Mainly used for node cleanup. We can remove all the "Declarator stub nodes. They were mainly there
        to handle typeSpecifier hierarchy
        """
        if self._declarator_node is not None:
            node = self._declarator_node.find_id()
            if node is not None:
                self._id = node.value
                self._filename = node.filename
                self._line = node.line
                self._column = node.column

        if self._declarator_node is not None:
            self._declarator_node.first_pass()

        if self._rhs_node is not None:
            self._rhs_node.first_pass()

    def semantic_analysis(self) -> bool:
        """
        On a declaration, a new identifier is introduced into the scope. This has to be an unique identifier
        on this scope lvl. But it can overshadow higher scoped (global...) declared variables with the same identifier.
        :return: true if successfully added identifier and children are semantically correct.
        """
        ret = True
        # First we need to pack the identifier's attributes. We have the base type and id trough reference of
        # the remaining decelerators we can deduce the type stack.
        if self._declarator_node is not None:
            self.type_stack = self._declarator_node.generate_type_operator_stack()

        # We have all the info for the corresponding attribute object
        attr = Attributes(self._base_type, self.type_stack, self._filename, self._line, self._column)

        # Now we need to check if there are no violations on the operators.
        # 1) Ptr type requires address of same type on the right side, NO IMPLICIT CONVERSIONS.
        if len(self.type_stack) > 0 and self.type_stack[-1].PTR:
            pass
        # 2) Explicit list init if array has no init size if type is array .
        if len(self.type_stack) > 0 and self.type_stack[-1] is DeclaratorSpecifier.ARRAY:
            # Last element is top of the stack.
            if not self._declarator_node.array_has_length():  # If array size is not specified MUST have array init rhs.
                if self._rhs_node is None:
                    if not isinstance(self._parent_node, ParamListNode):
                        messages.error_array_size_missing(self._id, attr)
                        ret = False

            if self._rhs_node is not None:  # The rhs of an array is an init list {0,1 ,2 3, 4}
                if not isinstance(self._rhs_node, ArrayInitNode):
                    tpl = self._rhs_node.get_error_info()
                    t_file = attr.filename
                    attr.filename = tpl[0]
                    t_line = attr.line
                    attr.line = tpl[1]
                    t_column = attr.column
                    attr.column = tpl[2]
                    messages.error_invalid_initializer(self._id, attr)
                    attr.filename = t_file
                    attr.line = t_line
                    attr.column = t_column
                    ret = False

        # Functions are allowed to be declared but definitions are not handled by this node
        elif len(self.type_stack) > 0 and self.type_stack[-1] is DeclaratorSpecifier.FUNC:
            if self._rhs_node is not None:
                messages.error_func_initialized_like_var(self._id, attr)
                ret = False
            attr.function_signature = self._declarator_node.get_function_signature()
        # Add to the scopes symbol_table.

        if not self.add_to_scope_symbol_table(self._id, attr):
            ret = False

        if self._rhs_node is not None and not self._rhs_node.semantic_analysis():
            ret = False

        return ret

    def implicit_param_ptr_conversion(self):
        """ int main(int *rgv []) == int main(int **argv)"""
        if self._declarator_node:
            self._declarator_node.implicit_param_ptr_conversion()

    def generate_llvm(self) -> str:
        """"
        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}
        """
        ptr = ""
        ptr += "*" * len(self.type_stack[:-1])  # TODO: This is not correct need ot handle this better
        ret = self.indent_string() + "; Declaration: {0}{1} {2}\n".format(self.base_type.value, ptr, self.id)
        # Special types need other llvm code first
        if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.ARRAY:
            # Find the type
            size = 0
            if self._rhs_node:
                size = self._rhs_node.size()  # Size of array if declared trough list
            r_type = self._base_type.llvm_type + ptr
            secondary_type = "[ " + str(size) + " x " + r_type + " ]"  # This is how we init an array
            ret += self.indent_string() + "%{0} = alloca {1}\n".format(
                self._id, secondary_type, self.base_type.llvm_alignment)

        else:
            ret += LlvmCode.llvm_allocate_instruction(self.id, self.base_type, self.type_stack, self.indent_string())

        if self._rhs_node is not None:
            ret += self.indent_string() + "; = ...\n"
            ret += self._rhs_node.generate_llvm()
            ret += LlvmCode.llvm_store_instruction(
                self.base_type,
                str(self.register_index),
                self.type_stack,

                self.base_type,
                self.id,
                self.type_stack,
                self.indent_string()
            )
        ret += self.indent_string() + "; end declaration\n"
        return ret
