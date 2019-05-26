from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode, ExpressionNodeType


class LHSNode(ExpressionNode):

    _BASE_LABEL = "LHS"

    def __init__(self, parent_node):
        super().__init__(parent_node)
        self._lhs_node = None

    def add_child(self, child: AbstractNode):

        if isinstance(child, LHSNode):
            self._lhs_node = child
        super().add_child(child)

    def find_id(self):
        if self.type is ExpressionNodeType.IDENTIFIER:
            self._parent_node.remove_child(self)
            return self.identifier

        elif self._lhs_node is not None:
            return self._lhs_node.find_id()


