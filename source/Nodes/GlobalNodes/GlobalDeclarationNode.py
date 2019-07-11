"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import LlvmCode
import Specifiers
from Attributes import AttributesGlobal
from Nodes.DeclarationNodes import DeclarationNode
from SymbolTable import GlobalActions
from messages import MessageGenerator


class GlobalDeclarationNode(DeclarationNode.DeclarationNode):
    _BASE_LABEL = "GlobalDeclaration"

    _DEFAULT_VALUE_MAP = {
        Specifiers.TypeSpecifier.INT: 0,
        Specifiers.TypeSpecifier.FLOAT: 0.0,
        Specifiers.TypeSpecifier.CHAR: 0,
        Specifiers.TypeModifier.PTR: "null"
    }

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)

    def semantic_analysis(self, messenger: MessageGenerator):

        # Globals need a compile time constant.
        defined = False
        if self._expression_node:

            if not self._expression_node.is_constant():
                messenger.error_init_is_not_constant(self._filename, self._line, self._column)
                return False

            defined = True

        attribute = AttributesGlobal(self.base_type, self.type_stack, self._filename, self._line, self._column, defined)
        next_action = self.add_to_scope_symbol_table(self.id, attribute)

        if next_action == GlobalActions.DO_NOTHING:
            return True

        elif next_action == GlobalActions.REDEFINE_ERROR:

            return False

        else:
            print("Need to set the expression_node to the first declaration node.")
            pass

    def generate_llvm(self):

        ret = ""
        # Globals must be assigned, so 0 by default (maybe we could make a global decl node to split logic)
        val = ""
        if not self._type_modifier_node:
            val = self._expression_node.llvm_constant if self._expression_node else \
                self.__class__._DEFAULT_VALUE_MAP[self.base_type]

        else:
            val = self.__class__._DEFAULT_VALUE_MAP[self._type_stack[-1]]

        ret += self.indent_string() + "; Global declaration " + str(self.base_type.value) + " " + self.id + " = " + str(
            val) + "\n "
        ret += LlvmCode.llvm_allocate_instruction_global(self.id, self.base_type, self._type_stack, str(val),
                                                         self.indent_string())
        ret += self.indent_string() + "; end declaration" + "\n"

        return ret
