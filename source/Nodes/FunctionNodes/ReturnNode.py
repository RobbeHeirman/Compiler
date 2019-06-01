"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Specifiers import TypeSpecifier


class ReturnNode(NonLeafNode):
    label = "return"

    def __init__(self, parent_node: NonLeafNode):
        super().__init__(parent_node)

    @property
    def base_type(self):
        return TypeSpecifier.DEFAULT

    def generate_llvm(self):
        ret = self._children[0].generate_llvm()
        ret_type = self._parent_node.base_type
        ret += self.indent_string() + "ret {0} %{1}\n".format(ret_type.llvm_type, self.register_index)
        return ret

    def has_return(self):
        if self._children:
            return True
        return False
