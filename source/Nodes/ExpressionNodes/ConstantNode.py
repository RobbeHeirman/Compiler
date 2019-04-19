"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import re

from source.Nodes.ExpressionNodes.RHSLeafNode import RHSLeafNode
from source.Specifiers import TypeSpecifier


class ConstantNode(RHSLeafNode):

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)

    @property
    def label(self):
        return "\"{0}\"".format(str(self._value))

    def llvm_code_value(self):

        if re.search("'.'", self.value) is not None:
            return ord(self.value[1:2])

        elif re.search("[0-9]+\.[0-9]+", self.value) is not None:
            return float(self.value)

        else:
            return int(self.value)

    def llvm_type(self):

        if re.search("'.'", self.value) is not None:
            return TypeSpecifier('char').llvm_type

        elif re.search("[0-9]+\.[0-9]+", self.value) is not None:
            return TypeSpecifier('float').llvm_type

        else:

            return TypeSpecifier('int').llvm_type


