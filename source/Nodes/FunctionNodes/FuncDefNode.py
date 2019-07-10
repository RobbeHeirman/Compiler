"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import sys

from antlr4 import ParserRuleContext

import messages
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.AbstractNodes.ScopedNode as ScopedNode
import Nodes.FunctionNodes.ReturnNode as ReturnNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode


class FuncDefNode(ScopedNode.ScopedNode, DeclarationNode.DeclarationNode):
    _id: str

    def __init__(self, parent_node: AbstractNode.AbstractNode, filename, ctx):

        super().__init__(parent_node, filename, ctx)

        self._id = ctx.getText()
        self.base_type = None
        self._return_node = None

        self._type_stack = None

    @property
    def label(self):
        return 'Func def\nIdentifier: {0}\nReturn type {1}'.format(self._id, self.base_type.value)

    def add_child(self, child, index=None):

        if isinstance(child, ReturnNode.ReturnNode):
            self._return_node = child

        super().add_child(child, index)

    def _make_attribute(self):

        attr = super()._make_attribute()
        signature = self._children[0].get_function_signature()
        attr.function_signature = signature
        return attr

    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis of a function definition.
        1)The function and his signature needs to be added to the symbol
        Table of the upper scope.
        2) The parameters are declared variables belonging to the scope of this function.
        :return: If the semantic analysis is correct.
        """
        ret = super().semantic_analysis(messenger)


        if self._return_node and not self._return_node.has_return():
            messenger.error_non_void_return(self._id, self._filename, self._line, self._column)
            ret = False

        return ret

    def generate_llvm(self):
        self.increment_register_index()
        ret = self.indent_string() + "define {0} @{1}(".format(self.base_type.llvm_type, self._id)
        ret += "{0}){{\n".format(self._children[0].generate_llvm())
        AbstractNode.AbstractNode._indent_level += 1
        for child in self._children[1:]:
            ret += child.generate_llvm()

        if self._return_node is None:
            ret += self.indent_string() + "  ret {0} 0\n".format(self.base_type.llvm_type)

        ret += "}\n"

        if ret is False:
            self._error_counter += 1

        return ret
