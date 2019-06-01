"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Nodes.AbstractNodes.ScopedNode import ScopedNode
from Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from Nodes.FunctionNodes.ReturnNode import ReturnNode
from Specifiers import DeclaratorSpecifier
from SymbolTable import Attributes


class FuncDefNode(ScopedNode):
    _id: str
    _parent_node: NonLeafNode

    def __init__(self, parent_node: NonLeafNode, id_l: str, ptr_count: int, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node)

        self._id = id_l
        self._ptr_count = ptr_count
        self._base_type = None
        self._base_type_node = None
        self._return_node = None

        self._type_stack = None

        self._filename = filename
        start = ctx.start
        self._line = start.line
        self._column = start.column

    @property
    def label(self):
        ptr_label = "*" * self._ptr_count
        return 'Func def\nIdentifier: {0}\nReturn type {1}{2}'.format(self._id, self._base_type.value, ptr_label)

    @property
    def base_type(self):
        return self._base_type

    def add_child(self, child, index=None):

        if isinstance(child, BaseTypeNode):
            self._base_type_node = child
            self._base_type = child.value

        elif isinstance(child, ReturnNode):
            self._return_node = child

        super().add_child(child, index)

    def first_pass(self):

        self._base_type = self._base_type_node.value
        self.remove_child(self._base_type_node)
        self._base_type_node = None

        super().first_pass()

    def semantic_analysis(self) -> bool:
        """
        Semantic analysis of a function definition.
        1)The function and his signature needs to be added to the symbol
        Table of the upper scope.
        2) The parameters are declared variables belonging to the scope of this function.
        :return: If the semantic analysis is correct.
        """
        ret = True
        # 1) Add to the symbol table of the upper scope
        self._type_stack = [DeclaratorSpecifier.PTR for _ in range(self._ptr_count)]
        attr = Attributes(self._base_type, self._type_stack, self._filename, self._line, self._column)
        signature = self._children[0].get_function_signature()
        attr.function_signature = signature
        if not self._parent_node.add_to_scope_symbol_table(self._id, attr):
            ret = False

        # 2)
        for child in self._children:
            if not child.semantic_analysis():
                ret = False

        if self._return_node and not self._return_node.has_return():
            messages.error_non_void_return(self._id, attr)
            ret = False

        return ret


    def generate_llvm(self):
        self.increment_register_index()
        ret = self.indent_string() + "define {0} @{1}(".format(self._base_type.llvm_type, self._id)
        ret += "{0}){{\n".format(self._children[0].generate_llvm())
        AbstractNode._indent_level += 1
        for child in self._children[1:]:
            ret += child.generate_llvm()

        if self._return_node is None:
            ret += self.indent_string() + "  ret {0} 0\n".format(self._base_type.llvm_type)

        ret += "}\n"
        return ret
