"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import LlvmCode
import Specifiers
from Nodes.DeclarationNodes import DeclarationNode


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

    # Semantic analysis

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
