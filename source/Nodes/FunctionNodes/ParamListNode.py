"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode


class ParamListNode(NonLeafNode):
    label = "Param list"

    def __init__(self, parent_node):
        super().__init__(parent_node)

    def get_function_signature(self):
        return [child.to_attribute() for child in self._children]

    def get_signature_list(self):
        return [child.base_type for child in self._children]

    def semantic_analysis(self):

        ret = True
        for child in self._children:
            if not child.semantic_analysis():
                ret = False
        return ret
