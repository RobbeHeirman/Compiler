"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.DeclarationNodes.TypeModifierNode import TypeModifierNode
from Specifiers import TypeModifier


class ExpressionTypeModifierNode(TypeModifierNode):

    def __init__(self, parent_node, filename, ctx, modifier=None):
        super().__init__(parent_node, filename, ctx, modifier)

    def generate_type_operator_stack(self, node, messenger):
        if self._type_modifier_node:
            if not self._type_modifier_node.generate_type_operator_stack(node, messenger):
                return False

        # Meaning the Dereference operator
        if self.modifier_type == TypeModifier.PTR:
            if node.type_stack_ref().type_stack[-1].type_modifier == TypeModifier.PTR:
                # If we dereference the type loses it's 'ptr' type
                node.type_stack_ref().type_stack.pop()
                node.l_value = True

            else:
                print("TODO some error about can't dereference a non pointer type")
                return False

        # Ref operator value becomes an address
        elif self.modifier_type == TypeModifier.ADDRESS:
            if node.l_value:
                node.type_stack_ref().append(TypeModifier.PTR)
                node.l_value = False

            else:
                messenger.error_lvalue_required_addr_operand(node.filename, node.line, node.column)
                return False

        # Function call,
        elif self.modifier_type == TypeModifier.FUNC:

            if node.type_stack_ref()[-1].modifier_type == TypeModifier.FUNC:
                if self.get_function_signature() == node.type_stack_ref()[-1].get_function_signature():
                    node.type_stack_ref().pop()

                else:
                    print(self.get_function_signature())
                    print(node.type_stack_ref()[-1].get_function_signature())
                    print(f'{self._line}TODO something about wrong signatures')

            else:
                print("TODO some messages about no function callable")
                pass
        return True
