"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

# import LlvmCode
import LlvmCode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    id: str

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)
        self.id = ctx.getText()
        self._l_value = True  # As it's base form an identifier is an Lvalue

        self._type_stack = self.get_attribute(self.id).operator_stack

    @property
    def label(self) -> str:
        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    def semantic_analysis(self, messenger):

        self._generate_type_modifier_stack()  # the modifiers applied in the expression
        ret = True
        if self.is_in_table(self.id):
            attr = self.get_attribute(self.id)
            # Now we need to check if the operations done on the identifier are legal
            if not self._stack_analysis(messenger, attr.operator_stack):
                ret = False

                # if self.type_stack and self.type_stack[-1] is DeclaratorSpecifier.FUNC:  # Now check the signature
                #   if attr.rhs_same_signature(self._parent_node.get_function_signature(), attrib, attr,
                #                             self.identifier):
                #       pass
                #   else:
                #    ret = False

        else:
            messenger.error_undeclared_var(self.id, self.filename, self.line, self.column)

        return ret

    def generate_llvm(self):
        self.increment_register_index()
        ret = self.indent_string() + ";... {0}\n".format(self.id)
        ret += LlvmCode.llvm_load_instruction(self.base_type, self.id, self.type_stack, self.base_type,
                                              str(self.register_index), self.type_stack, self.indent_string())

        return ret
