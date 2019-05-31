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
        to_load_index = self.register_index
        self.increment_register_index()
        ret += self.indent_string() + "%{0} = load {1}, {2}* %{3}, align {4}\n".format(self.register_index,
                                                                                       ret_type.llvm_type,
                                                                                       ret_type.llvm_type,
                                                                                       to_load_index,
                                                                                       ret_type.llvm_alignment)
        ret += self.indent_string() + "ret {0} %{1}\n".format(ret_type.llvm_type, self.register_index)
        return ret

    def has_return(self):
        if self._children:
            return True
        return False
