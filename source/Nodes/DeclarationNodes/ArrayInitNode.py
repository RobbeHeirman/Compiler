"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode


class ArrayInitNode(AbstractNode):
    label = "Array Init"
    _children: List[ExpressionNode]

    def __init__(self, parent_node):
        super().__init__(parent_node)

    def size(self):
        return len(self._children)

    def generate_llvm(self):
        ret = ""
        for index, child in enumerate(self._children):
            ret += child.generate_llvm()
            loading_index = self.register_index
            self.increment_register_index()
            array_type = "[ " + str(len(self._children)) + " x " + str(self._parent_node.type_string_llvm[:-1]) + " ]"
            ret += self.indent_string() + "%" + str(self.register_index) + " = getelementptr " + array_type + ", " \
                   + array_type + "* %" + self._parent_node.id + ", i32 0, i32 " + str(index) + "\n"

            ret += self.indent_string() + "store " + child.type_string_llvm + " %" + str(loading_index) + ", " \
                   + self._parent_node.type_string_llvm[:-1] + "* %" + str(self.register_index) + "\n"

        return ret
