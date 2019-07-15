"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Specifiers
from Nodes.ExpressionNodes.ExpressionNode import ExpressionNode
from Nodes.GlobalNodes.StatementsNode import StatementsNode


class ReturnNode(AbstractNode.AbstractNode):
    label = "return"

    def __init__(self, parent_node: AbstractNode.AbstractNode, filename, ctx):
        super().__init__(parent_node, filename, ctx)

    @property
    def base_type(self):
        return Specifiers.TypeSpecifier.DEFAULT

    def semantic_analysis(self, messenger):

        child = self._children[0]
        child.semantic_analysis(messenger)

        self._parent_node: StatementsNode

        ret_tuple = self._parent_node.get_return_type()
        child: ExpressionNode
        if not child.base_type == ret_tuple[0] or not child.type_stack == ret_tuple[1]:
            print(messenger.error_conflicting_return_type(self._filename, self._line, self._column))


    # def generate_llvm(self):
    #     ret = self._children[0].generate_llvm()
    #     ret_type = self._parent_node.base_type
    #     ret += self.indent_string() + "ret {0} %{1}\n".format(ret_type.llvm_type, self.register_index)
    #     return ret

    def has_return(self):
        if self._children:
            return True
        return False
