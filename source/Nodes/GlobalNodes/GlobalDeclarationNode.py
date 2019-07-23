"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import LlvmCode
import type_specifier
import Attributes
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
import SymbolTable
import messages


class GlobalDeclarationNode(DeclarationNode.DeclarationNode):
    _BASE_LABEL = "GlobalDeclaration"

    _DEFAULT_VALUE_MAP = {
        type_specifier.TypeSpecifier.INT: 0,
        type_specifier.TypeSpecifier.FLOAT: 0.0,
        type_specifier.TypeSpecifier.CHAR: 0,
        type_specifier.TypeSpecifier.POINTER: "null",
        type_specifier.TypeSpecifier.FUNCTION: "null"
    }

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

    def semantic_analysis(self, messenger: messages.MessageGenerator):

        if not self._generate_type_modifier_stack(messenger):
            return False

        defined = False

        if self._expression_node:
            # Expression semantics still need to be right
            if not self._expression_node.semantic_analysis(messenger):
                return False

            # Need a constant
            if not self._expression_node.is_constant():
                messenger.error_init_is_not_constant(self._line, self._column)
                return False

            self.analyze_initializer(messenger)

            defined = True

        attribute = Attributes.AttributesGlobal(self._type_stack, self._line, self._column,
                                                defined,
                                                self)

        # Function types have something extra, their function signature need to be recorded
        if self._type_stack and self._type_stack[-1] == type_specifier.TypeSpecifier.FUNCTION:
            function_signature = self._type_modifier_node.get_function_signature()

            attribute.function_signature = function_signature

        self._add_to_table(attribute, messenger)

        # adding to the parent's symbol table prevents from global nodes with own symbol tables to add themselves.

    def _add_to_table(self, attribute, messenger) -> bool:
        """
        The actions performed by response of the symbol table are the same for all global declarations
        :param attribute:
        :return:
        """
        next_action = self._parent_node.add_to_scope_symbol_table(self.id, attribute)
        if next_action == SymbolTable.GlobalActions.DO_NOTHING:
            return True

        elif next_action == SymbolTable.GlobalActions.REMOVE_NODE:

            # OPT: some redeclaration's just don't do anything, we can remove those nodes from the AST
            self._parent_node.remove_child(self)

            return True

        elif next_action == SymbolTable.GlobalActions.REDEFINE_ERROR:
            messenger.error_redefinition(self._line, self._column, self.id)
            return False

        elif next_action == SymbolTable.GlobalActions.WRONG_TYPE:
            messenger.error_conflicting_types(self._line, self._column, self.id)
            return False

        else:  # next action == DEFINE_PREV_DECLARED
            prev_declare: Attributes.AttributesGlobal = self.get_attribute(self.id)
            prev_declare.original_declaration_node.add_child(self._expression_node)
            # This node is obsolete afterwards
            self._parent_node.remove_child(self)

        return True

    def generate_llvm(self, is_comment: bool):

        ret = ""
        val = self._expression_node.llvm_constant if self._expression_node else \
            self.__class__._DEFAULT_VALUE_MAP[self._type_stack[-1].modifier_type]

        ret += self.code_indent_string() + "; Global declaration " + str(
            self.type_stack[0]) + " " + self.id + " = " + str(
            val) + "\n "
        ret += LlvmCode.llvm_allocate_instruction_global(self.id, self._type_stack, str(val),
                                                         self.code_indent_string())
        ret += self.code_indent_string() + "; end declaration" + "\n"

        return ret
