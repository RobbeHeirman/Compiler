"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Specifiers


class ParamListNode(AbstractNode.AbstractNode):
    label = "Param list"

    def __init__(self, parent_node):
        super().__init__(parent_node)

    def get_function_signature(self):
        return [child.to_attribute() for child in self._children]

    def get_signature_list(self):
        return [child.base_type for child in self._children]

    def semantic_analysis(self, messenger):

        ret = True
        for child in self._children:
            if not child.semantic_analysis:
                ret = False
        return ret

    def generate_llvm(self):
        ret = ""
        for child in self._children:

            ret += "{0}".format(child.base_type.llvm_type)
            for d_type in child.type_stack:
                if d_type is Specifiers.DeclaratorSpecifier.PTR:
                    ret += "*"
            ret += " %{0}".format(child.id)

            ret += ", "
        ret = ret[:-2]
        return ret
