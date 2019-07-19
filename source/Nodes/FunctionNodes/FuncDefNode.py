"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.AbstractNodes.ScopedNode as ScopedNode
import Nodes.GlobalNodes.GlobalDeclarationNode as GlobalDeclarationNode
import Attributes
import type_specifier
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Nodes.GlobalNodes.StatementsNode


class FuncDefNode(GlobalDeclarationNode.GlobalDeclarationNode, ScopedNode.ScopedNode):
    _id: str

    def __init__(self, parent_node: AbstractNode.AbstractNode, filename, ctx):
        super().__init__(parent_node, filename, ctx)

        self._param_list_node = None
        self._function_signature = []

    @property
    def label(self):
        return 'Func def\nIdentifier: {0}\nReturn type {1}'.format(self.id, [el.value for el in
                                                                             self._type_stack[:-1]])

    @property
    def base_type(self):
        return self._type_stack[0]

    @base_type.setter
    def base_type(self, tp):
        self._type_stack.append(tp)

    def add_child(self, child, index=None):

        if isinstance(child, Nodes.GlobalNodes.StatementsNode.StatementsNode):
            self._expression_node = child

        elif isinstance(child, ParamListNode.ParamListNode):
            self._param_list_node = child

        super().add_child(child, index)

    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis of a function definition.
        1)The function and his signature needs to be added to the symbol
        Table of the upper scope.
        2) The parameters are declared variables belonging to the scope of this function.
        :return: If the semantic analysis is correct.
        """
        # Check if the children are playing nice

        if not self._param_list_node.semantic_analysis(messenger):
            return False

        self._generate_type_modifier_stack(messenger)
        self._type_stack.append(type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.FUNCTION,
                                                             self._param_list_node.get_function_signature()))

        self._function_signature = self._param_list_node.get_function_signature()
        attribute = Attributes.AttributesGlobal(self._type_stack, self._filename, self._line, self._column,
                                                True,
                                                self)

        attribute.function_signature = self._function_signature
        if not self._add_to_table(attribute, messenger):
            return False

        for child in self._children:
            if child is not self._param_list_node:
                if not child.semantic_analysis(messenger):
                    return False
        return True

    def get_return_type(self):

        return self._type_stack[:-1]

    def generate_llvm(self):
        self.increment_register_index()
        ret = self.indent_string() + "define {0} @{1}(".format(self.base_type.llvm_type, self.id)
        ret += "{0}){{\n".format(self._children[0].generate_llvm())
        self.__class__._indent_level += 1
        for child in self._children[1:]:
            ret += child.generate_llvm()

        # if self._return_node is None:
        #     ret += self.indent_string() + "  ret {0} 0\n".format(self.base_type.llvm_type)

        ret += "}\n"
        self.__class__._indent_level -= 1
        return ret
