"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Nodes.AbstractNodes.AbstractNode as AbstractNode


class BinaryExpressionNode(ExpressionNode.ExpressionNode, ABC):
    """
    Base class for all Binary expression's
    """

    # Built ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._left_expression: ExpressionNode.ExpressionNode = None
        self._right_expression: ExpressionNode.ExpressionNode = None

    # AST-Generation
    # ==================================================================================================================

    def add_child(self, child: AbstractNode.AbstractNode, index=0):
        """
        Only wants 2 expression children, So we add the first one added to the left Expression Node the second
        one to the right. This follow's the order of the parse tree
        :param child: Node we want to add
        :param index: in a certain parent order
        """

        if isinstance(child, ExpressionNode.ExpressionNode):
            if not self._left_expression:
                self._left_expression = child
            elif not self._right_expression:
                self._right_expression = child
            else:
                raise IndexError("Adding a 3d expression to a binary expression")

        super().add_child(child, index)

    # Semantic-analysis
    # ==================================================================================================================

    def semantic_analysis(self, messenger) -> bool:
        """
        Checking the types of bother expression's mainly
        :param messenger:
        :return:
        """

        if not super().semantic_analysis(messenger):
            return False

        if self._left_expression.type_stack != self._right_expression.type_stack:
            # print(f'{self._left_expression.type_stack} :}')
            messenger.error_no_conversion_base_types(self._left_expression.type_stack[0],
                                                     self._right_expression.type_stack[0],
                                                     self.line,
                                                     self.column
                                                     )
            return False

        self._type_stack = self._left_expression.type_stack  # Expression adapt's type
        return True
