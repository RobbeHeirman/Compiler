"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Union, TYPE_CHECKING
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import type_specifier

if TYPE_CHECKING:
    import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class ParamListNode(AbstractNode.AbstractNode):
    label = "Param list"
    _children: Union[List['DeclarationNode.DeclarationNode'], List['ExpressionNode.ExpressionNode']]

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

            ret += "{0}".format(child.type_stack[0])
            for d_type in child.type_stack:
                if d_type == type_specifier.TypeSpecifier.POINTER:
                    ret += "*"
            ret += " %{0}".format(child.id)

            ret += ", "
        ret = ret[:-2]
        return ret
