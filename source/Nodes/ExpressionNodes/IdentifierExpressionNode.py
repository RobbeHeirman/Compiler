"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

# import LlvmCode
import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
from Specifiers import TypeSpecifier


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    id: str

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)
        self.id = ctx.getText()
        self._l_value = True  # As it's base form an identifier is an Lvalue

    @property
    def label(self) -> str:

        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    def semantic_analysis(self, messenger):
        self._type_stack = self.get_attribute(self.id).operator_stack
        self._generate_type_modifier_stack(messenger)  # the modifiers applied in the expression
        if not self.is_in_table(self.id):
            messenger.error_undeclared_var(self.id, self._filename, self._line, self._column)
            return False
        return True

    def generate_llvm(self):
        self.increment_register_index()
        ret = self.indent_string() + ";... {0}\n".format(self.id)
        ret += LlvmCode.llvm_load_instruction(self.id, self.type_stack, str(self.register_index), self.type_stack,
                                              self.indent_string())

        return ret
