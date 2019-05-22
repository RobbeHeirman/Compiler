"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
import messages as messages
from Specifiers import TypeSpecifier
from SymbolTable import Attributes


class AssignmentNode(ExpressionNode):

    def __init__(self, parent_node, id_name: str, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node)

        self._id = id_name
        self._base_type = None
        if not self._parent_node.is_in_table(self._id):
            # attr = Attributes(TypeSpecifier.DEFAULT, filename, ctx.start.line, ctx.start.column)
            self._fail_switch(True)
            # messages.error_undeclared_var(self._id, attr)

        else:
            attr = self._parent_node.get_attribute(self._id)
            self._base_type = attr.type_spec

    @property
    def label(self):
        return '"{0}="'.format(self._id)

    @property
    def base_type(self):
        return self._base_type

    def generate_llvm(self):

        ret = self._children[0].generate_llvm()
        ret += 'store {0} %{1}, {2}* %{3}\n'.format(self._base_type.llvm_type,
                                                    self.register_index,
                                                    self._base_type.llvm_type,
                                                    self._id)
        return ret