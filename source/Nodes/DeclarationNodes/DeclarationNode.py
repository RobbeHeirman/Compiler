"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from Nodes.ExpressionNodes.ArrayInitNode import ArrayInitNode
from Nodes.ExpressionNodes.RHSNode import RHSNode
from Nodes.DeclarationNodes.DeclaratorNode import DeclaratorNode
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Specifiers import TypeSpecifier, DeclaratorSpecifier
from SymbolTable import Attributes
from typing import Union


class DeclarationNode(NonLeafNode):
    """
    Represents a Declaration in our abstract syntax tree.
    Will deduct the base type of the declaration in the first pass.
    Has 1 or 2 children a declarator (will become a stack of pre and postfix type specifiers after first pass)
    An optional initializer as 2d child.
    """
    _declarator_node: DeclaratorNode
    _rhs_node: RHSNode
    _lexeme: str

    _BASE_LABEL = "Declaration"

    def __init__(self, parent_node: NonLeafNode):
        super().__init__(parent_node)

        # The 2 child nodes
        self._declarator_node = None
        self._rhs_node = None
        self._base_type_node = None

        # Base info
        self._id = None  # Id can be deducted from children.
        self._base_type = None  # Base type gets passed from a decl_list node.

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

        if self._base_type_node is not None:
            ret += "{0}--{{".format(self._index)
            ret += "{0} ".format(self._base_type_node.index)
            ret += "}\n"

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

        elif isinstance(child, BaseTypeNode):
            self._base_type_node = child
            self._base_type = child.value
        else:
            print(type(child))
            print("something went wrong")
        super().add_child(child)

    def remove_child(self, child):

        if isinstance(child, DeclaratorNode):
            self._declarator_node = None

        if isinstance(child, BaseTypeNode):
            self._base_type_node = None

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

        if self._base_type_node is not None:
            self._base_type = self._base_type_node.value
            self.remove_child(self._base_type_node)

    def semantic_analysis(self) -> bool:
        """
        On a declaration, a new identifier is introduced into the scope. This has to be an unique identifier
        on this scope lvl. But it can overshadow higher scoped (global...) declared variables with the same identifier.
        :return: true if successfully added identifier and children are semantically correct.
        """

        ret = True
        # First we need to pack the identifier's attributes. We have the base type and id trough reference of
        # the remaining decelerators we can deduce the type stack.
        type_stack = []
        if self._declarator_node is not None:
            type_stack = self._declarator_node.generate_type_operator_stack()

        # We have all the info for the corresponding attribute object
        attr = Attributes(self._base_type, type_stack, self._filename, self._line, self._column)

        # Now we need to check if there are no violations on the operators.
        # 1) Explicit list init if array has no init size if type is array .
        if len(type_stack) > 0 and type_stack[-1] is DeclaratorSpecifier.ARRAY:  # Last element is top of the stack.

            if not self._declarator_node.array_has_length():  # If array size is not specified MUST have array init rhs.
                if self._rhs_node is None:
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
        elif len(type_stack) > 0 and type_stack[-1] is DeclaratorSpecifier.FUNC:
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

    def generate_llvm(self) -> str:
        """"
        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}
        """
        ret = ""

        # lexeme = self._declarator.value
        ret += "%{0} = alloca {1}, align {2}\n".format(self._id,
                                                       self._base_type.llvm_type,
                                                       self._base_type.llvm_alignment)
        if self._rhs_node is not None:
            ret += self._rhs_node.generate_llvm()
            ret += 'store {0} %{1}, {2}* %{3}\n'.format(self._base_type.llvm_type,
                                                        self.register_index,
                                                        self._base_type.llvm_type,
                                                        self._id)
        return ret
