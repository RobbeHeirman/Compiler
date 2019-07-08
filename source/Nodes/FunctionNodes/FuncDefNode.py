"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

import messages
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.AbstractNodes.ScopedNode as ScopedNode
import Nodes.FunctionNodes.ReturnNode as ReturnNode
import Specifiers
import Attributes


class FuncDefNode(ScopedNode.ScopedNode):
    _id: str

    def __init__(self, parent_node: AbstractNode.AbstractNode, id_l: str, ptr_count: int, filename: str,
                 ctx: ParserRuleContext):
        super().__init__(parent_node)

        self._id = id_l
        self._ptr_count = ptr_count
        self.base_type = None
        self._return_node = None

        self._type_stack = None

        self._filename = filename
        start = ctx.start
        self._line = start.line
        self._column = start.column

    @property
    def label(self):
        ptr_label = "*" * self._ptr_count
        return 'Func def\nIdentifier: {0}\nReturn type {1}{2}'.format(self._id, self.base_type.value, ptr_label)

    def add_child(self, child, index=None):

        if isinstance(child, ReturnNode.ReturnNode):
            self._return_node = child

        super().add_child(child, index)

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
        self._type_stack = [Specifiers.TypeModifier.PTR for _ in range(self._ptr_count)]
        attr = Attributes.Attributes(self.base_type, self._type_stack, self._filename, self._line, self._column,
                                     self.__class__._messages)
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
