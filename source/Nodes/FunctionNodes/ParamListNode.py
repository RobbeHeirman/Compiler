"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Specifiers
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode


class ParamListNode(AbstractNode.AbstractNode):
    label = "Param list"

    def __init__(self, parent_node):
        super().__init__(parent_node)

    def get_function_signature(self):
        self._children: List[DeclarationNode]
        return [child.type_stack for child in self._children]

    def get_signature_list(self):
        self._children: List[DeclarationNode]
        return [child.base_type for child in self._children]


    def generate_llvm(self):
        ret = ""
        for child in self._children:
            child: DeclarationNode.DeclarationNode
            ret += "{0}".format(child._type_stack[0])
            for d_type in child.type_stack:
                if d_type is Specifiers.TypeModifier.PTR:
                    ret += "*"
            ret += " %{0}".format(child.id)

            ret += ", "
        ret = ret[:-2]
        return ret
