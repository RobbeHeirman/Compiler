"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.ExpressionNodes.LHSNode as LhsNode
from antlr4 import ParserRuleContext


class AssignmentNode(AbstractNode.AbstractNode):

    _BASE_LABEL = "="

    def __init__(self, parent_node, filename: str, ctx: ParserRuleContext):
        super().__init__(parent_node)

        self._id = None
        self._lhs_node = None

        attr = self._parent_node.get_attribute(self._id)
        if attr:
            self._base_type = attr.type_spec

    @property
    def label(self):
        ret = self._BASE_LABEL

        if self._id is not None:
            ret += "\n Identifier: {0}".format(self._id)

        return ret

    def add_child(self, child: AbstractNode.AbstractNode, index=None):
        if isinstance(child, LhsNode.LHSNode):
            self._lhs_node = child
        super().add_child(child)

    def _find_id(self):
        self._id = self._lhs_node.find_id()

    def first_pass(self):

        super().first_pass()
        self._find_id()

    def generate_llvm(self):

        ret = self._children[0].generate_llvm()
        ret += 'store {0} %{1}, {2}* %{3}\n'.format(self._base_type.llvm_type,
                                                    self.register_index,
                                                    self._base_type.llvm_type,
                                                    self._id)
        return ret
